from utils import *

def shortest_paths(rooms):
  dist = defaultdict(partial(defaultdict, partial(float, 'inf')))

  for a, adj in rooms.items():
    for b in adj:
      dist[a][b] = 1
    dist[a][a] = 0
  for thru in rooms:
    for src in rooms:
      for dst in rooms:
        dist[src][dst] = min(dist[src][thru] + dist[thru][dst], dist[src][dst])
  return dist

def main(data, raw):
  valves = {}
  rooms = {}
  for line in data:
    name = re.search('^Valve (\w+)', line)[1]
    rate = int(re.search('=(-?\d+)', line)[1])
    exits = re.search('leads? to valves? ((\w+(, )?)+)', line)[1]
    rooms[name] = exits.split(', ')
    if rate > 0:
      valves[name] = rate

  dist = shortest_paths(rooms)

  @lru_cache
  def max_flow(flow, time, current, unopened):
    return max(
      (
        max_flow(
          flow + valves[dst] * remain,
          remain, dst, unopened - {dst}
        )
        for dst in unopened
        if (remain := time - dist[current][dst] - 1) > 0
      ),
      default=flow
    )

  yield max_flow(0, 30, 'AA', frozenset(valves))

  def partitions(valves):
    n = len(valves)
    progress = [0] + [math.comb(n, i) for i in range(1, n//2 + 1)]
    for cardinality in range(1, n//2 + 1):
      for subset in combinations(valves, cardinality):
        # capture generator so it can be iterated multiple times
        subset = frozenset(subset)
        yield subset, frozenset(valves) - subset
      print(f'{progress[cardinality]/sum(progress):.2%} ({progress[cardinality]} / {sum(progress)})', end='\r')
    print()

  yield max(
    max_flow(0, 26, 'AA', subset)
    + max_flow(0, 26, 'AA', complement)
    for subset, complement in partitions(valves)
  )

if __name__ == '__main__':
  raw = '''
Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II
'''.strip('\n')

  sample = to_data(raw)
  for ans in main(sample, raw):
    print(ans)
