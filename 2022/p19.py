from utils import *

class Resource(NamedTuple):
  geode: int = 0
  obsidian: int = 0
  clay: int = 0
  ore: int = 0

  def __add__(self, other):
    if isinstance(other, Resource):
      return self.__class__(*(sum(mat) for mat in zip(self, other)))
  
  def __sub__(self, other):
    if isinstance(other, Resource):
      return self.__class__(*(a - b for a, b in zip(self, other)))
  
  def __mul__(self, other):
    if isinstance(other, int):
      return self.__class__(*(other * mat for mat in self))

class Robots(Resource):

  def build(self, robot: int):
    return self.__class__(*(
      v + (1 if i == robot else 0)
      for i, v in enumerate(self)
    ))

class Blueprint(NamedTuple):
  geode: Resource
  obsidian: Resource
  clay: Resource
  ore: Resource

  @lru_cache
  def max_bots(self):
    return Robots(*(
      max(mat) or float('inf')
      for mat in zip(*self)
    ))

def max_geode(time, blueprint, mats=Resource(), bots=Robots(ore=1)):
  max_bots = blueprint.max_bots()
  q = [(0, time, mats, bots)]
  seen = set()
  best_geode = 0
  while q:
    _, time, mats, bots = heapq.heappop(q)
    geode = mats.geode + bots.geode * time
    # if we produce geode bot every min
    optimistic = geode + (time - 1) * time // 2
    if optimistic < best_geode or (mats, time, bots) in seen:
      continue
    seen.add((mats, time, bots))
    best_geode = max(geode, best_geode)
    for bot, bp in enumerate(blueprint):
      if any(need and not has for need, has in zip(bp, bots)):
        continue
      # has enough bots
      if max_bots[bot]*time <= bots[bot]*time + mats[bot]:
        continue

      dt = 1 + next((i for i in range(time) if all(need <= willhave for need, willhave in zip(bp, mats + bots * i))), time)
      remain = time - dt
      if remain <= 0:
        continue
      dmat =  mats + bots * dt - bp
      dbots = bots.build(bot)
      heapq.heappush(q, (-1*dmat, remain, dmat, dbots))
      # prioritize geode if can materials available
      if dt == 1 and bp == blueprint.geode:
        break
  return best_geode


@timing
def main(data, raw):
  blueprints = {}
  for blueprint in data:
    name, bps = blueprint.split(':')
    name = int(re.search('(\d+)', name)[1])
    bp = defaultdict(Counter)
    for line in bps.split('.')[:-1]:
      bot, costs = line.split(' costs ')
      bot = re.search('Each (\w+) robot', bot)[1]
      for mat in costs.strip('.').split(' and '):
        amount, mat = mat.split(' ')
        bp[bot][mat] = int(amount)
    blueprints[name] = Blueprint(**{bot: Resource(**mats) for bot, mats in bp.items()})
  yield sum(name*max_geode(24, bp) for name, bp in blueprints.items())
  part2 = {i: max_geode(32, blueprints[i]) for i in range(1, 4)}
  yield part2[1] * part2[2] * part2[3]


if __name__ == '__main__':
  raw = '''
Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian.
'''.strip('\n')

  sample = to_data(raw)
  for ans in main(sample, raw):
    print(ans)
