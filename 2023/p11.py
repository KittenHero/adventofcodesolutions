from utils import *

def distance_sum(galaxies):
  return sum(manhattan(a, b) for a,b in combinations(galaxies, 2))

def manhattan(a, b):
  c = b - a
  return int(abs(c.real) + abs(c.imag))

@timing
def main(data, raw):
  galaxies = [
    x + 1j*y
    for y, row in enumerate(data)
    for x, space in enumerate(row)
    if space == '#'
  ]
  yield distance_sum(expand_empty(galaxies, 2))
  yield distance_sum(expand_empty(galaxies, 1e6))

def expand_empty(image, scale):
  def project_cur(cur, prev, projected_prev):
    if cur == prev:
      return projected_prev
    else:
      return (projected_prev + 1 + scale*(cur - prev - 1))

  image.sort(key=lambda c: c.imag)
  expanded_y = [ image[0].real + 1j*scale*image[0].imag ]
  for prev, cur in zip(image, image[1:]):
    expanded_y.append(cur.real + 1j*project_cur(cur.imag, prev.imag, expanded_y[-1].imag))

  expanded_y.sort(key=lambda c: c.real)
  expanded = [ scale * expanded_y[0].real + 1j*expanded_y[0].imag ]
  for prev, cur in zip(expanded_y, expanded_y[1:]):
    expanded.append(project_cur(cur.real, prev.real, expanded[-1].real) + 1j*cur.imag)

  return expanded

raw = '''
...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
'''.strip('\n')

if __name__ == '__main__':
  sample = to_data(raw)
  for ans in main(sample, raw):
    print(ans)
