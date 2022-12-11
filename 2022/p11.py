from utils import *

@dataclass
class Monkey:
  name: int
  items: List[int]
  op: List[str]
  test: int
  success: int
  fail: int

  inspected: int = 0

  @classmethod
  def from_text(cls, text):
    name, items, op, test, success, fail = text.split('\n')
    name, test, success, fail = [int(re.search(r'\d+', txt)[0]) for txt in [name, test, success, fail]]
    items = [int(n) for n in re.findall(r'\d+', items)]
    op = op.split('new = ')[1].split(' ')
    return cls(name=name, items=items, op=op, test=test, success=success, fail=fail)

  def turn(self, lcm=0):
    self.inspected += len(self.items)
    for item in self.items:
      updated = self.inspect(item) % lcm if lcm else self.inspect(item) // 3
      yield self.success if updated % self.test == 0 else self.fail, updated
    self.items = []

  def inspect(self, item):
    a, op, b = self.op
    assert a == 'old' and (b.isdigit() or b == 'old'), self.op
    return ops[op](item, int(b) if b.isdigit() else item)


def monkey_business(monkeys, *, rounds, relax=False):
  monkeys = copy.deepcopy(monkeys)
  lcm = 0 if relax else math.lcm(*(monkey.test for monkey in monkeys))
  for _ in range(rounds):
    for monkey in monkeys:
      for thrown, item in monkey.turn(lcm=lcm):
        monkeys[thrown].items.append(item)
  a, b = sorted([m.inspected for m in monkeys], reverse=True)[:2]
  return a * b


def main(data, raw):
  monkeys = [Monkey.from_text(monkey) for monkey in raw.split('\n\n')]
  yield monkey_business(monkeys, rounds=20, relax=True)
  yield monkey_business(monkeys, rounds=10000, relax=False)


if __name__ == '__main__':
  raw = '''
Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
'''.strip('\n')

  sample = to_data(raw)
  for ans in main(sample, raw):
    print(ans)
