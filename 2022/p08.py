from utils import *


def main(data, raw):
    grid = {
      (x,y): int(tree) 
      for y, row in enumerate(data)
      for x, tree in enumerate(row)
    }
    w, h = len(data[0]), len(data)
    stack = [
      ((0, i), (1, 0), -1) for i in range(h) # right
    ] + [
      ((w-1, i), (-1, 0), -1) for i in range(h) # left
    ] + [
      ((i, 0), (0, 1), -1) for i in range(w) # down
    ] + [
      ((i, h-1), (0, -1), -1) for i in range(w) # up
    ]
    visible = set()
    scenic = defaultdict(dict)
    while stack:
      pos, direction, tallest = stack.pop()
      if pos not in grid:
        continue
      height = grid[pos]
      (x, y), (dx, dy) = pos, direction
      stack.append(((x + dx, y + dy), direction, max(height, tallest)))
      # part 1
      if height > tallest:
        visible.add(pos)
      # part 2
      backwards = (x - dx, y - dy)
      if backwards not in grid:
        scenic[pos][direction] = 0
      else:
        score = 1
        while height > grid[backwards] and (bscore := scenic[backwards][direction]):
          score += bscore
          x, y = backwards
          backwards = (x - dx*bscore, y - dy*bscore)
        scenic[pos][direction] = score

    yield len(visible)
    yield max(reduce(op.mul, scenic[tree].values()) for tree in scenic)

if __name__ == '__main__':
  raw = '''
30373
25512
65332
33549
35390
'''.strip('\n')

  sample = to_data(raw)
  for ans in main(sample, raw):
    print(ans)
