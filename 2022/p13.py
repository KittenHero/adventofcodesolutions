from utils import *
import json

def cmp(a, b):
  match [a, b]:
    case [int(), int()]:
      return a - b
    case [list(), list()]:
      return next(
        (
          val for x,y in zip(a,b)
          if (val := cmp(x, y)) != 0
        ),
        len(a) - len(b)
      )
    case [list(), int()]:
      return cmp(a, [b])
    case [int(), list()]:
      return cmp([a], b)

def main(data, raw):
  pairs = [[json.loads(line) for line in pairs.split('\n')]  for pairs in raw.split('\n\n')]
  yield sum(i for i, (a,b) in enumerate(pairs, start=1) if cmp(a, b) < 0)

  dividers = ([[2]], [[6]])
  packets = sorted(list(chain(*pairs)) + list(dividers), key=cmp_to_key(cmp))
  a, b = [i for i,packet in enumerate(packets, start=1) if packet in dividers]
  yield a * b

if __name__ == '__main__':
  raw = '''
[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]
'''.strip('\n')

  sample = to_data(raw)
  for ans in main(sample, raw):
    print(ans)
