from utils import *

@timing
def main(data, raw):
  for plan in zip(*[dig_plan(row) for row in data if row]):
    yield area_gauss_shoelace(to_vertices(plan))

hexpattern = r'\(#([0-9a-f]{6})\)'
directions = {'U':-1j, 'D': 1j, 'L':-1, 'R':1}

def dig_plan(row):
  d, n, c = row.split(' ')
  return (directions[d], int(n)), hex_to_plan(c)

def hex_to_plan(color):
  hexadec = re.findall(hexpattern, color)[0]
  return  directions['RDLU'[int(hexadec[-1])]], int(hexadec[:-1], 16)

def area_gauss_shoelace(verts):
  return abs(int(0.5 * sum(
    p.real*q.imag - q.real*p.imag
    for p, q in zip(verts, verts[1:])
  )))

def to_vertices(plan):
  # add convexity to account for discretised area
  trench = [0]
  for (d, n), c in zip(plan, convexity(plan)):
    trench.append(trench[-1] + d*n + d*c)
  assert trench[-1] == 0
  return trench

def convexity(plan):
  # clockwise
  chirality = [a[0] == -1j*b[0] for a, b in zip(plan,  plan[1:] + plan[0:1])]
  return [
    (a == b) * (1 if a == chirality[0] else -1)
    for a,b in zip(
      chirality[-1:] + chirality[:-1],
      chirality
    )
  ]

raw = '''
R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)
'''.strip('\n')

if __name__ == '__main__':
  sample = to_data(raw)
  for ans in main(sample, raw):
    print(ans)
