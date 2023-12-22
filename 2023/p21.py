from utils import *

@timing
def main(data, raw):
  h = sum(map(bool, data))
  w = len(data[0])
  s = next(x + 1j * y for y, row in enumerate(data) if row for x, ch in enumerate(row) if ch == 'S')
  rocks = set(x + 1j * y for y, row in enumerate(data) if row for x, ch in enumerate(row) if ch == '#')

  y = []
  reachable = Reachable({s}, set())
  for i in range(131*2 + 65):
    if i == 64:
      yield len(reachable)
    reachable = reachable.step(rocks, w, h)

  n = 26501365
  # there is a clear path in cardinal directions
  assert all(s.real + 1j*k not in rocks for k in range(h)) and all(k + 1j*s.imag not in rocks for k in range(w))
  # edges are clear
  assert all(1j*k not in rocks and w - 1 + 1j*k not in rocks for k in range(h)) and all(k not in rocks and k + 1j*(h-1) not in rocks for k in range(w))
  # there are paths with width 5 connecting midpoints of adjacent edges
  assert all(
    (s.real - k - q)%w + 1j*(k%h) not in rocks
    and (s.real + k + q)%w+ 1j*(k%h) not in rocks
    for k in range(h) for q in range(-2, 3)
  )
  assert w == h == 131 and s == 65 + 65j and (n - 65) % 131 == 0 and (n // 131) % 2 == 0
  yield extrapolate(subdivide(reachable, w), n//131)


def subdivide(reachable, w):
  super_grid = defaultdict(int)
  for p in reachable:
    z = p.real//w + 1j*(p.imag//w)
    super_grid[z] += 1
  return super_grid

def extrapolate(super_grid, n):
  '''
      _
    _|_|_
  _|_|_|_|_
 |_|_|_|_|_|
  _|_|_|_|_
    _|_|_
      _
  '''
  corners = sum(super_grid[c] for c in [2, 2j, -2, -2j])
  edge_even = sum(super_grid[c] for c in [2+1j, -1+2j, -2-1j, 1-2j])
  edge_odd = sum(super_grid[c] for c in [1+1j, 1-1j, -1+1j, -1-1j])
  middle_odd = super_grid[0]
  middle_even = super_grid[1]
  assert edge_even == sum(super_grid[c] for c in [2-1j, -1-2j, -2+1j, 1+2j])
  assert middle_even == super_grid[-1] == super_grid[1j] == super_grid[-1j]
  return corners + n*edge_even + (n-1)*edge_odd + middle_even*n**2 + middle_odd*(n - 1)**2

@dataclass
class Reachable:
  cur: Set[complex]
  seen: Set[complex]

  def step(self, rocks, w, h):
    return dataclass_replace(
      self,
      cur={
        p + q
        for p in self.cur
        for q in [1, 1j, -1, -1j]
        if (p + q).real%w + 1j*((p + q).imag%h) not in rocks
        and (p + q) not in self.seen
      },
      seen=self.cur | self.seen,
    )

  def __iter__(self):
    yield from self.cur
    p = next(iter(self.cur))
    parity = (p.real + p.imag) % 2
    yield from (p for p in self.seen if (p.real + p.imag) % 2 == parity)

  def __len__(self):
    return sum(1 for i in self)

  def __str__(self):
    grid = self.cur | self.seen_cur_parity
    startx = min(int(p.real) for p in grid)
    starty = min(int(p.imag) for p in grid)
    stopx = 1 + max(int(p.real) for p in grid)
    stopy = 1 + max(int(p.imag) for p in grid)
    return '\n'.join(''.join('O' if x + 1j*y in grid else '.' for x in range(startx, stopx)) for y in range(starty, stopy))

raw = '''
...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........
'''.strip('\n')

if __name__ == '__main__':
  sample = to_data(raw)
  for ans in main(sample, raw):
    print(ans)
