from utils import *
from contextlib import suppress

def part_number_indices(indices_grid, symbols):
  '''Get indices of numbers surrounding symbols'''
  return set(
    indices_grid[q]
    for pos in symbols
    for dx, dy in product([-1,0,1], repeat=2)
    if not (dx == dy == 0) and (q := pos + dx + 1j*dy) in indices_grid
  )

@timing
def main(data, raw):
  symbols = {}
  grid = {}
  numbers = []

  for y, line in enumerate(data):
    for match in re.finditer(r'[^\d\.]', line):
      symbols[match.start(0) + 1j*y] = match.group(0)
    for match in re.finditer(r'\d+', line):
      for i in range(match.start(0), match.end(0)):
        grid[i + 1j*y] = len(numbers)
      numbers.append(int(match.group(0)))

  yield sum(numbers[i] for i in part_number_indices(grid, symbols))
  yield sum(
    numbers[pni.pop()] * numbers[pni.pop()]
    for pos, val in symbols.items()
    if val == '*'
    and (pni := part_number_indices(grid, [pos]))
    and len(pni) == 2
  )

raw = '''
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
'''.strip('\n')

if __name__ == '__main__':
  sample = to_data(raw)
  for ans in main(sample, raw):
    print(ans)
