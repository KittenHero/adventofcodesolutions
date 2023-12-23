from utils import *

@timing
def main(data, raw):
  slopes = {
    x+1j*y: {'>': 1, 'v': 1j, '<': -1, '^': -1j}[ch]
    for y, row in enumerate(data) if row
    for x, ch in enumerate(row) if ch in '<v>^'
  }
  path = set(
    x + 1j*y
    for y, row in enumerate(data) if row
    for x, ch in enumerate(row) if ch != '#'
  )
  start = min(path, key=lambda p: p.imag)
  end = max(path, key=lambda p: p.imag)
  # NP-hard (17 CPU s)
  yield walk(start, end, path, slopes)
  yield walk(start, end, path, {})

def walk(start, end, path, slopes):
  intersections = to_graph(start, path, slopes)
  i = 0
  stack = [(0, start, set())]
  best_hike = 0
  while stack:
    steps, cur, hike = stack.pop()
    if cur == end and steps > best_hike:
        best_hike = steps
    for n, n_step in intersections.get(cur, {}).items():
      if n in hike: continue
      stack.append((steps + n_step, n, hike | {cur}))
  return best_hike

def to_graph(start, path, slopes):
  intersections = {}
  seen = set()
  stack = [(start, start, 0, set())]
  while stack:
    cur, last, steps, hike = stack.pop()
    neighbours = list(filter(lambda n: n not in hike,
      [cur + i for i in [1,1j,-1,-1j] if cur + i in path]
      if cur not in slopes else
      [cur + slopes[cur]]
    ))
    if len(neighbours) != 1:
      intersections.setdefault(last, {})[cur] = steps
      if cur in seen:
        continue
      seen.add(cur)
      neighbours = [
        cur + i for i in [1,1j,-1,-1j]
        if cur + i in path
        and (
          cur + i not in slopes
          or slopes[cur + i] != -i
        )
      ]
      stack.extend((n, cur, 1, {cur}) for n in neighbours)
    else:
      stack.extend((n, last, 1 + steps, hike | {cur}) for n in neighbours)
  return intersections

raw = '''
#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#
'''.strip('\n')

if __name__ == '__main__':
  sample = to_data(raw)
  for ans in main(sample, raw):
    print(ans)
