from utils import *

@timing
def main(data, raw):
  bricks = fall([Brick(*get_all_ints(row)) for row in data if row])
  reactions = {b: reaction(b, bricks) for b in bricks}
  yield sum(not reaction for reaction in reactions.values())
  yield sum(map(len, reactions.values()))

def fall(bricks):
  class Support(NamedTuple):
    supporting: Set[Brick]
    supported: Set[Brick]

  grid = {}
  supports = {}

  for b in sorted(bricks, key=lambda b: b.z):
    while b.z > 0 and all(p not in grid for p in b.voxels):
      b = b.shift(dz=-1)
    b = b.shift(dz=1)
    supports[b] = Support(set(), set())
    for p in b.shift(dz=-1).voxels:
      if p not in grid: continue
      supports[grid[p]].supporting.add(b)
      supports[b].supported.add(grid[p])
    grid |= {p: b for p in b.voxels}
  return supports

def reaction(to_remove, supports):
  stack = [to_remove]
  falling = set()
  while stack:
    cur = stack.pop()
    falling.add(cur)
    for b in supports[cur].supporting:
      if not supports[b].supported.issubset(falling): continue
      stack.append(b)
  return falling - {to_remove}

class Brick(NamedTuple):
  x: int
  y: int
  z: int
  x2: int
  y2: int
  z2: int

  @property
  def voxels(self):
    assert self.x <= self.x2 and self.y <= self.y2 and self.z <= self.z2
    return [
      (xx,yy,zz)
      for xx,yy,zz in product(
        range(self.x, self.x2+1),
        range(self.y, self.y2+1),
        range(self.z, self.z2+1)
      )
    ]

  def shift(self, dx=0, dy=0, dz=0):
    return self._replace(
      x=self.x+dx, x2=self.x2+dx,
      y=self.y+dy, y2=self.y2+dy,
      z=self.z+dz, z2=self.z2+dz
    )

raw = '''
1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9
'''.strip('\n')

if __name__ == '__main__':
  sample = to_data(raw)
  for ans in main(sample, raw):
    print(ans)
