from utils import *

def chunk(data, size):
  return zip(*(data[i::size] for i in range(size)))

def main(data, raw):
  x = [1]
  samples = [cycle for cycle in range(20, 221, 40)]
  for line in data:
    match line.split(' '):
      case ['noop']:
        x.append(x[-1])
      case ['addx', num] if re.match(r'-?\d+', num):
        x.append(x[-1])
        x.append(x[-1] + int(num))

  yield sum([x[cycle-1]*cycle for cycle in samples])

  screen = ['#' if abs((i % 40) - v) <= 1 else ' ' for i, v in enumerate(x)]
  print('\n'.join(''.join(row) for row in chunk(screen, 40)))
  # submit part 2 manually

if __name__ == '__main__':
  raw = '''
addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop
'''.strip('\n')

  sample = to_data(raw)
  for ans in main(sample, raw):
    print(ans)
