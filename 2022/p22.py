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
  #yield explore(maze, inst, cube_wrap(maze))

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
