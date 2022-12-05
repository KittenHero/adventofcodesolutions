from utils import *


def main(data, raw):
  stack_raw, proc = map(lambda s: s.split('\n'), raw.split('\n\n'))
  *_, n = get_all_ints(stack_raw[-1])
  stack = [
    [
      crate for line in reversed(stack_raw[:-1])
      if (crate := line[4*col + 1]) not in '[ ]'
    ]
    for col in range(n)
  ]
  actual = [[c for c in col] for col in stack]

  for line in proc:
    count, src, dst = get_all_ints(line)
    src -= 1
    dst -= 1

    stack[dst].extend(reversed(stack[src][-count:]))
    del stack[src][-count:]

    actual[dst].extend(actual[src][-count:])
    del actual[src][-count:]

  yield ''.join(col[-1] for col in stack)
  yield ''.join(col[-1] for col in actual)

if __name__ == '__main__':
  raw = '''
    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
'''.strip('\n')

  sample = to_data(raw)
  for ans in main(sample, raw):
    print(ans)
