from utils import *

rocks = [
  [(i, 0) for i in range(4)],
  [(1, 2),(0, 1),(1, 1),(2, 1),(1, 0)],
  [(0, 0),(1, 0),(2, 0),(2, 1),(2, 2)],
  [(0, i) for i in range(4)],
  [(0, 0),(0, 1),(1, 0),(1, 1)],
]

def translate_all(rock, dx=0, dy=0):
  return [
    (x + dx, y + dy) for x,y in rock
  ]

def display(shape, rock=[]):
  print_grid({(x,-y): '#' if y > 0 else '-' for x,y in shape} | {(x,-y): '@' for x,y in rock})

def relative_top(top):
  ymax = max(top)
  return tuple(y - ymax for y in top)

def main(data, raw):
  shape = {(i, 0) for i in range(7)}
  top = [0 for i in range(7)]
  tallest = max(top)
  jet = 0
  history = {}
  trillion = 1_000_000_000_000
  for i in range(trillion):
    if i == 2022:
      yield tallest
    j = i%len(rocks)
    rock = translate_all(rocks[j], dx=2, dy=tallest + 4)

    # repeating stream, rock, & top shape
    rel = relative_top(top)
    if (j, jet, rel) in history:
      previ, prevtallest = history[(j, jet, rel)]
      # skip to the end
      if (trillion - i) % (i - previ) == 0 and i >= 2022:
        tallest += (tallest - prevtallest) * (trillion - i)//(i - previ)
        yield tallest
        break
    else:
      history[(j, jet, rel)] = i, tallest
    
    while True:
      match raw[jet]:
        case '<':
          dx = -1
        case '>':
          dx = 1
      jet = (jet + 1)%len(raw)
      moved = translate_all(rock, dx=dx)
      if not any(x < 0 or x >= 7 or (x, y) in shape for x, y in moved):
        rock = moved
      moved = translate_all(rock, dy=-1)
      if not any(p in shape for p in moved):
        rock = moved
      else:
        shape.update(rock)
        top = [
          max((y for x,y in rock if x == i and y > top[i]), default=top[i])
          for i in range(7)
        ]
        tallest = max(top)
        break
      key = ()
  

if __name__ == '__main__':
  raw = '''
>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>
'''.strip('\n')

  sample = to_data(raw)
  for ans in main(sample, raw):
    print(ans)
