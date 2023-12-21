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


manual_solution = '''
broadcaster -> sj, sr, tp, nk

0b111100101001 = 3881
%sj -> kj, rb       1
%kj -> fk           0
%fk -> xh           0
%xh -> zs, rb       1
%zs -> ct           0
%ct -> rt, rb       1
%rt -> hq           0
%hq -> bb           0
%bb -> kf, rb       1
%kf -> rb, ph       1
%ph -> rb, hx       1
%hx -> rb           1
&rb -> vc, zs, fk, hq, rt, sj, kj
&vc -> lg

0b111100001011 = 3851
%sr -> vs, ml       1
%vs -> tq, ml       1
%tq -> jm           0
%jm -> ml, kp       1
%kp -> vk           0
%vk -> tk           0
%tk -> sh           0
%sh -> zk           0
%zk -> ml, ps       1
%ps -> qz, ml       1
%qz -> ml, kh       1
%kh -> ml           1
&ml -> kp, sr, tq, nb, tk, sh, vk
&nb -> lg

0b111101100111 = 3943
%tp -> gp, lx       1
%lx -> ff, gp       1
%ff -> gp, df       1
%df -> nv           0
%nv -> xm           0
%xm -> gp, cq       1
%cq -> gp, mq       1
%mq -> pr           0
%pr -> gp, pf       1
%pf -> gp, nt       1
%nt -> gs, gp       1
%gs -> gp           1
&gp -> df, ls, mq, tp, nv
&ls -> lg

0b111101011011 = 3931
%nk -> nn, bt       1
%nn -> xf, bt       1
%xf -> qr           0
%qr -> bt, zt       1
%zt -> pb, bt       1
%pb -> kq           0
%kq -> tl, bt       1
%tl -> bn           0
%bn -> sv, bt       1
%sv -> dx, bt       1
%dx -> bt, tz       1
%tz -> bt           1
&bt -> tl, nk, pb, xf, vg
&vg -> lg

LCM(3881, 3851, 3931, 3943) = 231657829136023
&lg -> rx
'''