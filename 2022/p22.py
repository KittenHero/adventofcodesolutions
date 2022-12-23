from utils import *


def explore(maze, inst, topology):
  pos = min(maze, key=lambda p: (p.imag, p.real))
  facing = 1
  path = {}
  f2v = {1:'>', -1:'<', 1j:'V', -1j:'^'}
  for i in inst:
    match i:
      case 'L' | 'R':
        facing *= {'R': 1j, 'L': -1j}[i]
      case int():
        for _ in range(i):
          pos, facing = topology(pos, facing, maze)
          path[pos] = f2v[facing]
    path[pos] = f2v[facing]
  #print_grid(maze | path | {pos: '@'}, empty=' ')
  return int(pos.imag + 1)*1000 + int(pos.real + 1)*4 + [1, 1j, -1, -1j].index(facing)


def simple_wrap(pos, facing, maze):
  step = pos + facing
  tile = maze.get(step, ' ')

  if tile == ' ':
    step = complex(
      pos.real if facing.real == 0 else facing.real * min(
        facing.real * p.real for p in maze if p.imag == pos.imag
      ),
      pos.imag if facing.imag == 0 else facing.imag * min(
        facing.imag * p.imag for p in maze if p.real == pos.real
      ),
    )
    tile = maze[step]
  if tile == '#':
    return pos, facing
  if tile == '.':
    return step, facing


@timing
def main(data, raw):
  maze, inst = raw.split('\n\n')
  inst = list(chain(*[(int(n), r) for n, r in re.findall('(\d+)(L|R)?', inst)]))
  maze = {
    x + y * 1j: tile for y, row in enumerate(maze.split('\n'))
    for x, tile in enumerate(row)
    if tile in '.#'
  }
  yield explore(maze, inst, simple_wrap)
  yield explore(maze, inst, cube_wrap(maze))

def match_L_edges(offsets, cube_width):
  unconnected = defaultdict(list)
  wrapping = {}
  for i, pos in enumerate(offsets):
    for d in [1, 1j, -1, -1j]:
      p = pos + cube_width * d
      if p not in offsets:
        unconnected[p].append((i, d))
      else:
        wrapping[i, d] = (offsets.index(p), d)

  for p, u in unconnected.items():
    match u:
      case [(o1, d1), (o2, d2)]:
        wrapping[o1, d1] = (o2, -d2)
        wrapping[o2, d2] = (o1, -d1)
        o3 = offsets[o1] + d2*cube_width
        o4 = offsets[o2] + d1*cube_width
        # match L tail
        if o3 in offsets and not o4 in offsets:
          o3 = offsets.index(o3)
          wrapping[o3, d1] = (o2, -d1)
          wrapping[o2, d1] = (o3, -d1)
        elif o3 not in offsets and o4 in offsets:
          o4 = offsets.index(o4)
          wrapping[o4, d2] = (o1, -d2)
          wrapping[o1, d2] = (o4, -d2)
      case [(o1, d1)]:
        pass
      case []:
        pass
      case _:
        assert False, u
  return wrapping

def clockwise_edges(cur, offsets, cube_width, seen):
  if cur in seen:
    return
  seen.add(cur)
  for d in [1, 1j, -1, -1j]:
    p = offsets[cur] + d * cube_width
    if p not in offsets:
      yield cur, d
    else:
      yield from clockwise_edges(
        offsets.index(p),
        offsets,
        cube_width,
        seen
      )

def match_edges(offsets, cube_width):
  wrapping = match_L_edges(offsets, cube_width)
  # see 22.png step 3
  unmatched = []
  for face, direction in clockwise_edges(0, offsets, cube_width, set()):
    if (face, direction) in wrapping:
      continue
    unmatched.append((face, direction))
    if len(unmatched) == 1:
      continue
    (fa, da), (fb, db) = unmatched[-2:]
    if fa == fb or any(fsrc == fa and fdst == fb for (fsrc, _), (fdst, _) in wrapping.items()):
      continue
    wrapping[fa, da] = (fb, -db)
    wrapping[fb, db] = (fa, -da)
    del unmatched[-2:]
  return wrapping

def cube_wrap(maze):
  cube_width = int((len(maze) // 6) ** 0.5)
  offsets = [
    pos for pos in maze
    if pos.real % cube_width == 0 == pos.imag % cube_width
  ]
  wrap = match_edges(offsets, cube_width)

  def cube_face(pos):
    for i, p in enumerate(offsets):
      if (
        0 <= pos.real - p.real < cube_width
        and 0 <= pos.imag - p.imag < cube_width
      ):
        return i

  def wrap_rel(rx, direction):
    match direction:
      case 0:
        return rx
      case 1:
        return 0
      case -1:
        return cube_width - 1

  def topology(pos, facing, maze):
    step = pos + facing
    tile = maze.get(step, ' ')
    new_facing = facing

    if tile == ' ':
      face = cube_face(pos)
      rel = pos - offsets[face]
      face, new_facing = wrap[face, facing]

      if 1j * facing == new_facing: # R
        step = (
          wrap_rel(cube_width - rel.imag - 1, new_facing.real)
          + 1j * wrap_rel(rel.real, new_facing.imag)
          + offsets[face]
        )
      elif -1j * facing == new_facing: # L
        step = (
          wrap_rel(rel.imag, new_facing.real)
          + 1j * wrap_rel(cube_width - rel.real - 1, new_facing.imag)
          + offsets[face]
        )
      elif -1 * facing == new_facing: # U-turn
        step = (
          wrap_rel(cube_width - rel.real - 1, new_facing.real)
          + 1j * wrap_rel(cube_width - rel.imag - 1, new_facing.imag)
          + offsets[face]
        )
      elif facing == new_facing:
        step = (
          wrap_rel(rel.real, new_facing.real)
          + 1j* wrap_rel(rel.imag, new_facing.imag)
          + offsets[face]
        )
      tile = maze[step]
    if tile == '#':
      return pos, facing
    if tile == '.':
      return step, new_facing

  return topology


raw = '''
        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5
'''.strip('\n')

if __name__ == '__main__':
  sample = to_data(raw)
  for ans in main(sample, raw):
    print(ans)
