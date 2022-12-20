from utils import *

def mix(q, rounds=1):
  original = q.copy()
  for _ in range(rounds):
    for enum in original:
      _, n = enum
      idx = q.index(enum)
      q.rotate(-idx)
      q.popleft()
      q.rotate(-n)
      q.appendleft(enum)
      if n == 0:
        zero = enum
  q.rotate(-q.index(zero))
  return sum(q[i*1000 % len(q)][1] for i in range(1, 4))

@timing
def main(data, raw):
  data = [int(line) for line in data]
  yield mix(deque(enumerate(data)), rounds=1)
  yield mix(deque((i, 811589153*n) for i, n in enumerate(data)), rounds=10)


if __name__ == '__main__':
  raw = '''
1
2
-3
3
-2
0
4
'''.strip('\n')

  sample = to_data(raw)
  for ans in main(sample, raw):
    print(ans)
