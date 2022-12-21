from utils import *

from fractions import Fraction

@dataclass
class LinearExpression:
  factors: dict
  constant: Fraction = 0

  @classmethod
  def from_symbol(cls, name: str):
    return cls(Counter(name))

  def __add__(self, other):
    if isinstance(other, Fraction) or isinstance(other, int):
      return self.__class__(self.factors, self.constant + other)
    if isinstance(other, self.__class__):
      return self.__class__(self.factors + other.factors, self.constant + other.constant)
    return NotImplemented
  
  __radd__ = __add__

  def __sub__(self, other):
    if isinstance(other, Fraction) or isinstance(other, int):
      return self.__class__(self.factors, self.constant - other)
    if isinstance(other, self.__class__):
      return self.__class__(self.factors - other.factors, self.constant - other.constant)
    return NotImplemented

  def __rsub__(self, other):
    # other - self = 
    return -1 * (self - other)

  
  def __mul__(self, other):
    if isinstance(other, Fraction) or isinstance(other, int):
      return self.__class__(
        Counter({ name: factor * other for name, factor in self.factors.items() }),
        self.constant * other
      )
    return NotImplemented

  __rmul__ = __mul__

  def __truediv__(self, other):
    if isinstance(other, Fraction):
      return self * Fraction(1, other)
    return NotImplemented

    ans = list(main(data, raw))

# or just from sympy import Symbol, solve
Symbol = LinearExpression.from_symbol


def solve(expression, symbol):
  name = next(name for name in symbol.factors)
  return - expression.constant / expression.factors[name]

ops = {
  '+': op.add,
  '*': op.mul,
  '-': op.sub,
  '/': op.truediv,
}

def expand_root(monkeys, jobs):
  monkeys = copy.deepcopy(monkeys)
  while 'root' not in monkeys:
    for name, (a, op, b) in jobs.items():
      if name in monkeys:
        continue
      if a not in monkeys or b not in monkeys:
        continue
      a, b = monkeys[a], monkeys[b]
      monkeys[name] = ops[op](a, b)
  return monkeys['root']

@timing
def main(data, raw):
  monkeys = {
    name: Fraction(int(n))
    for line in data
    for name, n in [line.split(': ')]
    if re.match(r'-?\d+', n)
  }
  jobs = {
    name: exp.split(' ')
    for line in data
    for name, exp in [line.split(': ')]
    if name not in monkeys
  }

  yield int(expand_root(monkeys, jobs))
  x = Symbol('x')
  monkeys['humn'] = x
  jobs['root'][1] = '-'
  yield int(solve(expand_root(monkeys, jobs), x))

raw = '''
root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32
'''.strip('\n')

if __name__ == '__main__':
  sample = to_data(raw)
  for ans in main(sample, raw):
    print(ans)
