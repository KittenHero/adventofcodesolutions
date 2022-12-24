from utils import *


@timing
def main(data, raw):
  while not data[-1]:
    del data[-1]

  walls = {
    x + 1j*y
    for y, line in enumerate(data)
    for x, ch in enumerate(line)
    if ch == '#'
  }
  blizzard = tuple(
    frozenset(
      x + 1j*y
      for y, line in enumerate(data)
      for x, ch in enumerate(line)
      if ch == b
    )
    for b in '>v<^'
  )
  directions = [1,1j,-1,-1j,0]
  start = data[0].index('.')
  goal = data[-1].index('.') + (len(data) - 1)*1j

  width = max(pos.real for pos in walls) - min(pos.real for pos in walls)
  height = max(pos.imag for pos in walls) - min(pos.imag for pos in walls)

  # prevent search from walking outside walls
  walls.add(start - 1j)
  walls.add(goal + 1j)

  def width_height(walls, d):
    if d.real:
      return  width
    elif d.imag:
      return height

  def search(start, blizzard, goal, t=0):
    q = {start}
    for i in count(start=t):
      if goal in q:
        return i, blizzard
      blizzard = tuple(
        frozenset(
          new_pos
          if (new_pos := pos + d) not in walls
          else new_pos - d *(width_height(walls, d) - 1)
          for pos in wind
        )
        for d, wind in zip(directions, blizzard)
      )
      q = {
        new_pos
        for pos in q
        for d in directions
        if (new_pos := pos + d) not in walls
        and all(new_pos not in b for b in blizzard)
      }

  t, blizzard = search(start, blizzard, goal, 0)
  yield t
  t, blizzard = search(goal, blizzard, start, t)
  t, blizzard = search(start, blizzard, goal, t)
  yield t

raw = '''
#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#
'''.strip('\n')

if __name__ == '__main__':
  sample = to_data(raw)
  for ans in main(sample, raw):
    print(ans)
