from utils import *

def has_neighbor(elf, elves):
  return any(
    elf + x + 1j*y in elves
    and not (x == y == 0)
    for x, y in product([-1,0,1], repeat=2)
  )

def propose(e, elves, directions):
  return next(
    (
      d for d in directions
      if all(p not in elves for p in [e + d, e + d + 1j*d, e + d - 1j*d])
    ),
    0
  )

@timing
def main(data, raw):
  elves = set(
    x + 1j*y
    for y, row in enumerate(data)
    for x, ch in enumerate(row)
    if ch == '#'
  )
  directions = deque([-1j, 1j, -1, 1])

  for r in count(start=1):
    proposal =  {
      e: (
        e + propose(e, elves, directions)
        if has_neighbor(e, elves)
        else e
      )
      for e in elves
    }
    proposal_count = Counter(proposal.values())
    moved = set(
      p if proposal_count[p] == 1 else e
      for e, p in proposal.items()
    )
    directions.rotate(-1)

    if r == 20:
      width = 1 + max(int(p.real) for p in moved) - min(int(p.real) for p in moved)
      height = 1 + max(int(p.imag) for p in moved) - min(int(p.imag) for p in moved)
      yield width * height - len(moved)
    if moved == elves:
      break
    elves = moved

  yield r

raw = '''
....#..
..###.#
#...#.#
.#...##
#.###..
##.#.##
.#..#..
'''.strip('\n')

if __name__ == '__main__':
  sample = to_data(raw)
  for ans in main(sample, raw):
    print(ans)
