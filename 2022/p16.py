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
  start_room = 'AA'
  start_time = 30

  order = {key: i for i, key in enumerate(valves)}
  if start_room not in order:
    order[start_room] = len(valves)
  # list is ~4x faster than dict
  cache = [None]*2*31*len(order)*(2 << len(valves))
  def key(time, current, unopened, other):
    return other + 2*time + 2*31*order[current] + 2*31*len(order)*sum(1 << order[dst] for dst in unopened)

  def max_flow(time, current, unopened, other):
    if all(dist[current][dst] + 1 >= time for dst in unopened):
      if not other:
        return 0
      else:
        return max_flow(start_time, start_room, unopened, other - 1)

    k = key(time, current, unopened, other)
    if cache[k] is None:
      cache[k] = max(
        chain(
          # do nothing (for part 2)
          [max_flow(0, current, unopened, other)],
          # open valve
          (
            valves[dst] * remain
            + max_flow(remain, dst, unopened - {dst}, other)
            for dst in unopened
            if (remain := time - dist[current][dst] - 1) > 0
          ),
        ),
        default=0
      )
    return cache[k]

  yield max_flow(start_time, start_room, frozenset(valves), 0)
  start_time = 26
  yield max_flow(start_time, start_room, frozenset(valves), 1)


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
