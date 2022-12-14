from utils import *

def fall_steps(x, y):
  yield x, y + 1
  yield x - 1, y + 1
  yield x + 1, y + 1

def has_support(x, y, grid):
  return any(x == px and py > y for px, py in grid)

def has_floor_support(floor):

  def has_support(x, y, grid):
    return floor > y + 1
  
  return has_support

def next_step(sand, grid, has_support):
  if not has_support(*sand, grid):
    return
  for step in fall_steps(*sand):
    if step in grid:
      continue
    return step

def sand_fall(sand, grid, has_support):
  while (step := next_step(sand, grid, has_support)):
    sand = step
  return sand

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
    sand = sand_fall(source, grid, has_support)
    if not has_support(*sand, grid):
      break
    grid[sand] = 'o'
  
  yield i
  floor = floor = 2 + max(y for (x, y), item in grid.items() if item == '#')
  for j in count():
    if source in grid:
      break
    grid[sand_fall(source, grid, has_floor_support(floor))] = 'o'
  yield i + j


if __name__ == '__main__':
  raw = '''
498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
'''.strip('\n')

  sample = to_data(raw)
  for ans in main(sample, raw):
    print(ans)
