from utils import *

def sand_fall_positions(x, y):
  yield x, y + 1
  yield x - 1, y + 1
  yield x + 1, y + 1

def has_support(x, y, grid):
  return any(x == px and py > y for px, py in grid)

def has_floor_support(x, y, grid):
  floor = 2 + max(y for (x, y), item in grid.items() if item == '#')
  return floor > y + 1

def next_fall(sand, grid, has_support):
  if not has_support(*sand, grid):
    return
  for step in sand_fall_positions(*sand):
    if step in grid:
      continue
    return step

def main(data, raw):
  grid = {}

  for line in data:
    points = [[int(n) for n in re.findall(r'\d+', p)] for p in line.split('->')]
    for (px, py), (qx, qy) in zip(points, points[1:]):
      if px == qx:
        for y in range(min(py, qy), max(py, qy) + 1):
          grid[px, y] = '#'
      elif py == qy:
        for x in range(min(px, qx), max(px, qx) + 1):
          grid[x, py] = '#'
  
  source = 500, 0
  for i in count():
    sand = source
    while (falling := next_fall(sand, grid, has_support)):
      sand = falling
    if not has_support(*sand, grid):
      break
    grid[sand] = 'o'
  
  yield i
  for j in count():
    if source in grid:
      break
    sand = source
    while (falling := next_fall(sand, grid, has_floor_support)):
      sand = falling
    grid[sand] = 'o'
  yield i + j


if __name__ == '__main__':
  raw = '''
498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
'''.strip('\n')

  sample = to_data(raw)
  for ans in main(sample, raw):
    print(ans)
