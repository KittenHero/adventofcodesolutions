from utils import *

def adj(xyz):
  for sign, axis in product([-1,1], range(3)):
    yield tuple(sign * (axis == i) + p for i, p in enumerate(xyz))

def outside_surfaces(surfaces, lava):
  bounds = [
    [
      sign + sign*max(sign*p*(i == axis) for xyz in lava for i, p in enumerate(xyz))
      for sign in [-1, 1]
    ]
    for axis in range(3)
  ]
  # DFS/flood fill from a region on the boundary
  # the outside regions are all connected
  dfs = [next(xyz for xyz in surfaces if any(p in bounds[i] for i, p in enumerate(xyz)))]
  outside_lava = set()
  while dfs:
    cur = dfs.pop()
    if cur in outside_lava or cur in lava:
      continue
    # out of bounds
    if any(p < bounds[i][0] or bounds[i][1] < p for i, p in enumerate(cur)):
      continue
    outside_lava.add(cur)
    for ss in adj(cur):
      dfs.append(ss)
  return Counter(s for s in surfaces.elements() if s in outside_lava)

def main(data, raw):
  lava = set()
  for line in data:
    x,y,z = map(int, re.findall('-?\d+', line))
    lava.add((x,y,z))

  surfaces = Counter(n for cube in lava for n in adj(cube) if n not in lava)
  yield surfaces.total()
  yield outside_surfaces(surfaces, lava).total()


if __name__ == '__main__':
  raw = '''
2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5
'''.strip('\n')

  sample = to_data(raw)
  for ans in main(sample, raw):
    print(ans)
