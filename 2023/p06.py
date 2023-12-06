from utils import *

def ways_to_win(time, record):
  return sum(record < i*(time - i) for i in range(time))

def join_int(s):
  return int(''.join(re.findall(r'\d+', s)))

@timing
def main(data, raw):
  records = {
    int(time): int(dist)
    for time, dist in
    zip(*filter(bool, map(partial(re.findall, r'\d+'), data[:2])))
  }
  product = partial(reduce, op.mul)
  yield product(
    ways_to_win(dist, time)
    for time, dist in records.items()
  )
  yield ways_to_win(join_int(data[0]), join_int(data[1]))

raw = '''
Time:      7  15   30
Distance:  9  40  200
'''.strip('\n')

if __name__ == '__main__':
  sample = to_data(raw)
  for ans in main(sample, raw):
    print(ans)
