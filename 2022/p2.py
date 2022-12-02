from utils import *


def main(data, raw):
  scores = {
    'A X': 1+3,
    'B X': 1+0,
    'C X': 1+6,
    'A Y': 2+6,
    'B Y': 2+3,
    'C Y': 2+0,
    'A Z': 3+0,
    'B Z': 3+6,
    'C Z': 3+3,
  }

  yield sum(scores[line] for line in data if line)

  actual_score = {
    'A X': 3+0,
    'B X': 1+0,
    'C X': 2+0,
    'A Y': 1+3,
    'B Y': 2+3,
    'C Y': 3+3,
    'A Z': 2+6,
    'B Z': 3+6,
    'C Z': 1+6,
  }
  yield sum(actual_score[line] for line in data if line)

if __name__ == '__main__':
  raw = '''
A Y
B X
C Z
'''.strip()

  sample = to_data(raw)
  for ans in main(sample, raw):
    print(ans)
