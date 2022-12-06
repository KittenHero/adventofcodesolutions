from utils import *

def zip_consecutive(data, size):
  return zip(*(data[i:] for i in range(size)))

def find_unique_runs(data, size):
  for i, code in enumerate(zip_consecutive(data, size)):
    if len(set(code)) == size:
      yield i


def main(data, raw):
  yield 4 + next(find_unique_runs(raw, 4))
  yield 14 + next(find_unique_runs(raw, 14))

if __name__ == '__main__':
  raw = '''
mjqjpqmgbljsphdztnvjfqwrcgsmlb
'''.strip('\n')

  sample = to_data(raw)
  for ans in main(sample, raw):
    print(ans)
