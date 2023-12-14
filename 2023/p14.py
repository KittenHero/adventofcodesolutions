from utils import *

@timing
def main(data, raw):
  def copy(grid):
    return list(map(list, grid))

  grid = [list(row) for row in data if row]
  yield north_load(tilt_n(copy(grid)))
  yield north_load(cycle(grid, int(1e9)))

def north_load(grid):
  return sum(
    (elem == 'O') * (len(grid) - i)
    for i, row in enumerate(grid)
    for j, elem in enumerate(row)
  )


def cycle(grid, n):
  def snapshot(grid):
    return tuple(map(tuple, grid))
  def invert(d):
    return dict(map(reversed, d.items()))

  path = {}
  for i in range(n):
    s = snapshot(grid)
    if (k := path.get(s)) is not None:
      return invert(path)[k + (n - i)%(i - k)]

    path[s] = i
    for f in [tilt_n, tilt_w, tilt_s, tilt_e]:
      grid = f(grid)
  return grid

def tilt_n(grid):
  floor = [0] * len(grid[0])
  for i, row in enumerate(grid):
    for j, elem in enumerate(row):
      if elem == 'O' and floor[j] < i:
        row[j] = '.'
        grid[floor[j]][j] = 'O'
        floor[j] += 1
      elif elem == 'O' and floor[j] == i or elem == '#':
        floor[j] = i + 1
  return grid

def tilt_s(grid):
  return tilt_n(grid[::-1])[::-1]

def tilt_w(grid):
  for row in grid:
    floor = 0
    for j, elem in enumerate(row):
      if elem == 'O' and floor < j:
        row[j] = '.'
        row[floor] = 'O'
        floor += 1
      elif elem == 'O' and floor == j or elem == '#':
        floor = j + 1
  return grid

def tilt_e(grid):
  def reverse_inner(m):
    return list(map(lambda v: v[::-1], m))
  return reverse_inner(tilt_w(reverse_inner(grid)))

raw = '''
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
'''.strip('\n')

if __name__ == '__main__':
  sample = to_data(raw)
  for ans in main(sample, raw):
    print(ans)
