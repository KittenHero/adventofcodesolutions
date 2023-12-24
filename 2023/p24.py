from utils import *

@timing
def main(data, raw, begin=200000000000000, end=400000000000000):
  hailstones = [Vec(*get_all_ints(row)) for row in data if row]
  def point_in_region(p):
    return begin <= p.real <= end and begin <= p.imag <= end
  yield sum(
    point_in_region(p)
    for a, b in combinations(hailstones, 2)
    if (p := intersect_xy(a, b)) is not None
  )
  import z3
  solver = z3.Solver()
  x,y,z, dx,dy,dz = z3.Reals('x y z dx dy dz')
  for i, h in enumerate(hailstones[:3]):
    t = z3.Real(f't_{i}')
    solver.add(t > 0)
    solver.add(x + dx * t == h.x + h.dx * t)
    solver.add(y + dy * t == h.y + h.dy * t)
    solver.add(z + dz * t == h.z + h.dz * t)
  assert solver.check() == z3.sat
  m = solver.model()
  yield m.eval(x + y + z)

def intersect_xy(p, q):
  def general_form(vec):
    '''
    x(t) = t*dx + x0 
    t = (x(t) - x0)/dx = (y(t) - y0)/dy
    dy x(t) - dx y(t) + y0 dx - x0 dy = 0  
    '''
    return vec.dy, -vec.dx, vec.y*vec.dx - vec.x*vec.dy
  a, b, c = general_form(p)
  i, j, k = general_form(q)
  if a*j - i*b == 0:
    return None
  x = (b*k - j*c)/(a*j - i*b)
  y = (c*i - k*a)/(a*j - i*b)

  def ahead(p, x, y):
    return (x - p.x)/p.dx > 0 and (y - p.y)/p.dy > 0
  
  if not ahead(p, x, y) or not ahead(q, x, y):
    return None
  return x + 1j*y


class Vec(NamedTuple):
  x: int
  y: int
  z: int
  dx: int
  dy: int
  dz: int

raw = '''
19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3
'''.strip('\n')

if __name__ == '__main__':
  sample = to_data(raw)
  for ans in main(sample, raw, begin=7, end=27):
    print(ans)
