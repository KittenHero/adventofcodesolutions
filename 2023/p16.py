from utils import *

@timing
def main(data, raw):
  colliders = {
    x + 1j*y: ch
    for y, row in enumerate(data)
    for x, ch in enumerate(row)
    if ch != '.'
  }
  w = len(data[0])
  h = len([r for r in data if r])
  yield len(traverse(colliders, pos=0, vel=1, width=w, height=h))
  walls = {
    1: [1j * i for i in range(h)],
    1j: [i for i in range(w)],
    -1: [w - 1 + 1j * i for i in range(h)],
    -1j: [i + 1j * (h - 1) for i in range(w)]
  }
  yield max(
    len(traverse(colliders, pos=pos, vel=facing, width=w, height=h))
    for facing, wall in walls.items()
    for pos in wall
  )

def traverse(colliders, pos, vel, width, height):
  fringe = [(pos, vel)]
  path = set()
  while fringe:
    p, q = fringe.pop()
    if (p, q) in path or not (0 <= p.real < width and 0 <= p.imag < height):
      continue
    path.add((p, q))
    if p not in colliders:
      fringe.append((p + q, q))
    elif colliders[p] == '|' and q.real != 0:
      fringe.append((p + 1j, 1j))
      fringe.append((p - 1j, -1j))
    elif colliders[p] == '-' and q.imag != 0:
      fringe.append((p + 1, 1))
      fringe.append((p - 1, -1))
    elif colliders[p] == '/':
      q = q * -1j if q.real else q * 1j
      fringe.append((p + q, q))
    elif colliders[p] == '\\':
      q = q * 1j if q.real else q * -1j
      fringe.append((p + q, q))
    else:
      fringe.append((p + q, q))
  return set(pos for pos, vel in path)

def debug_path(path, colliders):
  print_cgrid({
    pos: {1:'>', -1:'<',1j:'V',-1j:'^'}[vel]
          if pos not in colliders
          else colliders[pos]
    for pos, vel in path
  })


raw = r'''
.|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....
'''.strip('\n')

if __name__ == '__main__':
  sample = to_data(raw)
  for ans in main(sample, raw):
    print(ans)
