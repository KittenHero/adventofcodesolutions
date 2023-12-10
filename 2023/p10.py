from utils import *

pipes = {
  '-': [1, -1],
  'F': [1j, 1],
  '|': [1j, -1j],
  '7': [1j, -1],
  'L': [-1j, 1],
  'J': [-1j, -1],
}

@timing
def main(data, raw):
  grid = {
    x + 1j *y: pipes[tile]
    for y, row in enumerate(data)
    for x, tile in enumerate(row)
    if tile in pipes
  }
  start = next(
    x + 1j *y
    for y, row in enumerate(data)
    for x, tile in enumerate(row)
    if tile == 'S'
  )

  for shape in pipes.values():
    loop = traverse(grid | {start: shape}, start)
    if not loop: continue
    yield len(loop) // 2
    yield len(enclosed_region(loop, grid | {start: shape}))


def traverse(grid, start):
  path = [start, start + grid[start][0]]
  if -grid[start][0] not in grid.get(path[-1], []):
    return
  while path[-1] != start:
    cur = path[-1]
    back = path[-2] - path[-1]
    pipe = grid.get(cur, [])
    forward = next(p for p in pipe if p != back)
    if -forward not in grid.get(cur + forward, []):
      return
    path.append(cur + forward)
  return set(path)


def enclosed_region(loop, grid):
  start_x = int(min(p.real for p in loop))
  stop_x = 1 + int(max(p.real for p in loop))
  start_y = int(min(p.imag for p in loop))
  stop_y = 1 + int(max(p.imag for p in loop))
  return [
    x + 1j*y
    for y in range(start_y, stop_y)
    for x in range(start_x, stop_x)
    if (x + 1j*y) not in loop
    and count_crossing(x + 1j*y, loop, grid) % 2 == 1
  ]


def count_crossing(p, loop, grid):
  crossable_edges = [
    grid[p - x - 1]
    for x in reversed(range(int(p.real)))
    if (p - x - 1) in loop
    and grid[p - x - 1] != pipes['-']
  ]
  return sum(
    a == pipes['|']
    or a == pipes['F'] and b == pipes['J']
    or a == pipes['L'] and b == pipes['7']
    for a, b in zip_longest(crossable_edges, crossable_edges[1:])
  )


raw = '''
FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L
'''.strip('\n')

if __name__ == '__main__':
  sample = to_data(raw)
  for ans in main(sample, raw):
    print(ans)
