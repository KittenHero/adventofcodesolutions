from utils import *

@dataclass(frozen=True)
class Vec2:
  x: int
  y: int

  def __add__(self, other):
    match other:
      case Vec2(a, b):
        return self.__class__(self.x + a, self.y + b)
      case _:
        return NotImplemented

  def __sub__(self, other):
    match other:
      case Vec2(a, b):
        return self.__class__(self.x - a, self.y - b)
      case _:
        return NotImplemented

  def sign(self):
    return self.__class__((self.x > 0) - (self.x < 0), (self.y > 0) - (self.y < 0))

  def adjacent(self, other):
    return abs(self.x - other.x) <= 1 and abs(self.y - other.y) <= 1

  def __iter__(self):
    yield self.x
    yield self.y

def main(data, raw):
  rope = [Vec2(0,0)] * 10
  directions = {
    'R': Vec2(1, 0),
    'L': Vec2(-1, 0),
    'U': Vec2(0, -1),
    'D': Vec2(0, 1),
  }
  visited = {rope[0]}
  tail = {rope[0]}
  for line in data:
    d, n = line.split(' ')
    for i in range(int(n)):
      rope[0] += directions[d]

      for j in range(9):
        a, b = rope[j], rope[j+1]
        if a.adjacent(b): continue
        b += (a - b).sign()
        rope[j+1] = b
      
      visited.add(rope[1])
      tail.add(rope[-1])

  yield len(visited)
  yield len(tail)

if __name__ == '__main__':
  raw = '''
R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
'''.strip('\n')

  sample = to_data(raw)
  for ans in main(sample, raw):
    print(ans)
