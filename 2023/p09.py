from utils import *

def extrapolate(line, dir=1):
  diff = [b - a for a, b in zip(line, line[1:])]
  next_diff = 0 if all(d == 0 for d in diff) else extrapolate(diff, dir)
  if dir == 1:
    return line[-1] + next_diff
  else:
    return line[0] - next_diff

@timing
def main(data, raw):
  data = [get_all_ints(line) for line in data if line]
  yield sum(extrapolate(line, dir=1) for line in data)
  yield sum(extrapolate(line, dir=-1) for line in data)

raw = '''
0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
'''.strip('\n')

if __name__ == '__main__':
  sample = to_data(raw)
  for ans in main(sample, raw):
    print(ans)
