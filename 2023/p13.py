from utils import *

@timing
def main(data, raw):
  data = [room.split('\n') for room in raw.strip('\n').split('\n\n')]
  yield sum(
    100*hsym(room) + vsym(room)
    for room in data
  )
  yield sum(
    100*hsym(room, smudge=1) + vsym(room, smudge=1)
    for room in data
  )

def vsym(room, smudge=0):
  w = len(room[0])
  for i in range(1, w):
    if smudge == sum(a != b for row in room for a,b in zip(row[:i][::-1], row[i:])):
      return i
  return 0

def hsym(room, smudge=0):
  h = len(room)
  for i in range(1, h):
    if smudge == sum(c != d for above,below in zip(room[:i][::-1], room[i:]) for c, d in zip(above, below)):
      return i
  return 0

raw = '''
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
'''.strip('\n')

if __name__ == '__main__':
  sample = to_data(raw)
  for ans in main(sample, raw):
    print(ans)
