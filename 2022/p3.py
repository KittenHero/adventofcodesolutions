from utils import *

def main(data, raw):
  yield sum(
    priority(common(*half_split(bag)))
    for bag in data
  )
  yield sum(
    priority(common(a,b,c))
    for a,b,c in chunk(data, 3)
  )

def priority(item):
  return ord(item) + (1 - ord('a') if 'a' <= item <= 'z' else 27 - ord('A'))

def common(*iterables):
  first, *rest = iterables
  return next(item for item in first if all(item in bag for bag in rest))

def half_split(bag):
  mid = len(bag) // 2
  return bag[:mid], bag[mid:]

def chunk(data, size):
  return zip(*(data[i::size] for i in range(size)))

if __name__ == '__main__':
  raw = '''
vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
'''.strip()

  sample = to_data(raw)
  for ans in main(sample, raw):
    print(ans)
