from utils import *


def score_vec(strength, card_order, hand):
  return [strength[5 - i] for i in range(5)] + [card_order.index(val) for val in hand]

def score(line):
  hand = line.split(' ')[0]
  strength = Counter(Counter(hand).values())
  return score_vec(strength, '23456789TJQKA', hand)

def wild_joker_score(line):
  hand = line.split(' ')[0]
  # wild joker
  melds = Counter(hand)
  # remove joker from hand first in case it is the most common card
  melds['J'] = 0
  melds[melds.most_common(1)[0][0]] += Counter(hand)['J']

  strength = Counter(Counter(melds).values())
  return score_vec(strength, 'J23456789TQKA', hand)


def bid(line):
  return int(line.split(' ')[1])

@timing
def main(data, raw):
  ranked = sorted(filter(bool, data), key=score)
  yield sum(rank * bid(line) for rank, line in enumerate(ranked, start=1))
  joker_ranked = sorted(filter(bool, data), key=wild_joker_score)
  yield sum(rank * bid(line) for rank, line in enumerate(joker_ranked, start=1))

raw = '''
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
'''.strip('\n')

if __name__ == '__main__':
  sample = to_data(raw)
  for ans in main(sample, raw):
    print(ans)
