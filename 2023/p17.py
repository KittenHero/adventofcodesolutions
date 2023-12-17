from utils import *

@timing
def main(data, raw):
  grid = {x + 1j*y: int(loss) for y, row in enumerate(data) for x, loss in enumerate(row)}
  end = next(reversed(grid.keys()))
  heuristic = estimator(grid, end)
  yield astar(grid, heuristic, 0, end, allowed_move=list(range(1, 4)))
  yield astar(grid, heuristic, 0, end, allowed_move=list(range(4, 11)))

# dijkstra
def estimator(grid, end):
  estimate = defaultdict(lambda: float('inf'))
  pq = PriorityQueue([(0, end)], key=lambda x: x[0])
  while pq:
    cost, cur = pq.pop()
    if cost >= estimate[cur]:
      continue
    estimate[cur] = cost
    for d in [1, 1j, -1, -1j]:
      if cur + d not in grid: continue
      pq.push((cost + grid[cur], cur + d))
  return estimate

def astar(grid, heuristic, start, end, allowed_move):
  pq = PriorityQueue(key=lambda x: x[0])
  pq.push((heuristic[start], 0, start, 1))
  pq.push((heuristic[start], 0, start, 1j))
  visited = set()
  while pq:
    estimate, cost, cur, prev_axis = pq.pop()
    if cur == end: return cost
    if (cur, prev_axis) in visited: continue
    visited.add((cur, prev_axis))
    axis = 1j if prev_axis == 1 else 1
    for d in [axis, -axis]:
      additional_cost = sum(grid.get(cur + d*i, 0) for i in range(1, allowed_move[0]))
      for k in allowed_move:
        pos = cur + d*k
        if pos not in grid: break
        additional_cost += grid[pos]
        total_cost = cost + additional_cost
        pq.push((total_cost + heuristic[pos], total_cost, pos, axis))

class PriorityQueue:
  def __init__(self, iterable=None, key=lambda x: x):
    self.key = key
    self.index = 0
    if iterable:
      self.data = [(key(item), i, item) for i, item in enumerate(iterable)]
      self.index = len(self.data)
      heapq.heapify(self.data)
    else:
      self.data = []

  def __repr__(self):
    return f'{self.__class__.__name__}({self.data})'
  
  def push(self, item):
    heapq.heappush(self.data, (self.key(item), self.index, item))
    self.index += 1

  def pop(self):
    return heapq.heappop(self.data)[-1]

  def __bool__(self):
    return bool(self.data)

raw = '''
2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533
'''.strip('\n')

if __name__ == '__main__':
  sample = to_data(raw)
  for ans in main(sample, raw):
    print(ans)
