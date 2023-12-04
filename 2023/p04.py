from utils import *

def count_winning(numbers):
    winning, has = map(partial(re.findall, r'\d+'), numbers.split(' | '))
    return sum(n in winning for n in has)

@timing
def main(data, raw):
  winning = [count_winning(line.split(': ')[1]) for line in data if line]
  yield sum(1 << count >> 1 for count in winning)

  cards = Counter()
  for i, count in enumerate(winning):
    cards[i] += 1
    for j in range(count):
      cards[i + 1 + j] += cards[i]
  yield cards.total()

raw = '''
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
'''.strip('\n')

if __name__ == '__main__':
  sample = to_data(raw)
  for ans in main(sample, raw):
    print(ans)
