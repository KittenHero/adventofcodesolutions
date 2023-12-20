from utils import *

@timing
def main(data, raw):
  destinations: Dict[str, List[str]] = {}
  flipflops: Dict[str, int] = {}
  conjunctions: Dict[str, Dict[str, int]] = {}

  for row in data:
    if not row: continue
    src, *dst = re.sub(r' -> |, ', ' ', row.strip('&%')).split(' ')
    destinations[src] = dst
    if row[0] == '%':
      flipflops[src] = 0
    elif row[0] == '&':
      conjunctions[src] = {}
  for src, dst in destinations.items():
    for d in dst:
      if d in conjunctions:
        conjunctions[d][src] = 0
  
  low = 0
  high = 0
  cycles: Dict[str, int] = {}

  for i in count(start=1):
    signals = deque([('button', ['broadcaster'], 0)])
    while signals:
      src, dest, pulse = signals.pop()
      low += (1 ^ pulse) * len(dest)
      high += pulse * len(dest)
      for d in dest:
        if d not in destinations: continue
        dest = destinations[d]
        if d == 'broadcaster':
          signals.appendleft((d, dest, pulse))
        elif d in flipflops and not pulse:
          flipflops[d] ^= 1
          signals.appendleft((d, dest, flipflops[d]))
        elif d in conjunctions:
          state = conjunctions[d]
          state[src] = pulse
          out = int(sum(state.values()) != len(state))
          signals.appendleft((d, dest, out))
          if sum(state.values()) == 0 and d not in cycles:
            cycles[d] = i

        # part 2
        if 'rx' in dest:
          assert d in conjunctions and all(s in conjunctions for s in conjunctions[d])
          state = conjunctions[d]
          if set(state).issubset(cycles):
            yield math.lcm(*(cycles[c] for c in state))
            return
    # part 1
    if i == 1000:
      yield low * high

raw = '''
broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a
'''.strip('\n')

raw = '''
broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output
'''.strip('\n')

if __name__ == '__main__':
  sample = to_data(raw)
  for ans in main(sample, raw):
    print(ans)
