from utils import *


class Edge(NamedTuple):
  L: str
  R: str


class Path(NamedTuple):
  length: int
  cycle_start: int
  possible_stops: List[int]

  @property
  def cycle_length(self):
    return self.length - self.cycle_start


def traverse(start, can_stop, directions, network):
  cur = start
  path = []
  for i, d in cycle(enumerate(directions)):
    pos = cur, i
    if pos in path:
      return Path(len(path), path.index(pos), [i for i, (q, _) in enumerate(path) if can_stop(q)])
    path.append(pos)
    cur = network[cur][d]

def modulo_inverse(a, n):
  a = a % n
  t, s = 0, 1
  r, rr = n, a
  while rr:
    (q, rr), r = divmod(r, rr), rr
    t, s = s, t - q * s
  t += n * (t < 0)
  return t

def sync_path_cycles(min_steps, cycle_lengths):
  super_cycle = math.lcm(*cycle_lengths)
  # chinese remainder theorem
  gcd = math.gcd(*cycle_lengths)
  moduli = [n // gcd for n in cycle_lengths]
  remainders = [s % n for s, n in zip(min_steps, moduli)]
  N = super_cycle
  N_i = [N // n for n in moduli]
  final_steps = sum(r * M * modulo_inverse(M, n)  for r, n, M in zip(remainders, moduli, N_i)) % N
  # add a super cycle if final_steps is 0 as it needs to be greater than min steps
  return final_steps + super_cycle * (final_steps == 0)

@timing
def main(data, raw):
  directions, network = raw.split('\n\n')

  network = {
    line.split(' = ')[0]: Edge(*line.split(' = ')[1][1:-1].split(', '))._asdict()
    for line in network.split('\n')
    if line
  }
  yield traverse('AAA', partial(op.eq, 'ZZZ'), directions, network).possible_stops[0]

  paths = [
    traverse(pos, lambda pos: pos.endswith('Z'), directions, network)
    for pos in network
    if pos.endswith('A')
  ]
  yield min(
    sync_path_cycles(*zip(*possible_stop))
    for possible_stop in product(*[
      [
        (stop, p.cycle_length)
        for stop in p.possible_stops
        if stop > p.cycle_start
      ]
      for p in paths
    ])
  )

raw = '''
LR

AAA = (11B, XXX)
11B = (XXX, ZZZ)
ZZZ = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
'''.strip('\n')

if __name__ == '__main__':
  sample = to_data(raw)
  for ans in main(sample, raw):
    print(ans)
