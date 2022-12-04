from utils import *


def main(data, raw):
  data = [[int(x) for pair in line.split(',') for x in pair.split('-')] for line in data]
  assert [a <= b and c <= d for a,b,c,d in data]
  # contained
  yield sum(a <= c <= d <= b or c <= a <= b <= d for a,b,c,d in data)
  # overlapped
  yield sum(a <= c <= b or a <= d <= b or c <= a <= d or c <= b <= d for a,b,c,d in data)

if __name__ == '__main__':
  raw = '''
2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
'''.strip()

  sample = to_data(raw)
  for ans in main(sample, raw):
    print(ans)
