from utils import *

@timing
def main(data, raw):
  workflows, parts = raw.strip('\n').split('\n\n')
  workflows = {row.split('{')[0]: row.split('{')[1].strip('}') for row in workflows.split('\n')}
  parts = [Part(*get_all_ints(row)) for row in parts.split('\n')]
  yield sum(p.x + p.m + p.a + p.s for p in parts if process_part('in', workflows, p))
  yield sum(r.combinations() for r in process_range('in', workflows, PartRange()))

def process_part(workflow, workflows, part):
  if workflow in 'RA':
    return workflow == 'A'
  for rule in workflows[workflow].split(','):
    if ':' not in rule:
      return process_part(rule, workflows, part)
    cond, workflow = rule.split(':')
    rating, comp, n = re.match(r'([xmas])([<>])(-?\d+)', cond).groups()
    if {'>': op.gt, '<': op.lt}[comp](getattr(part, rating), int(n)):
      return process_part(workflow, workflows, part)

class Part(NamedTuple):
  x: int
  m: int
  a: int
  s: int

def process_range(workflow, workflows, part_range):
  if not part_range or workflow == 'R':
    pass
  elif workflow == 'A':
    yield part_range
  else:
    for rule in workflows[workflow].split(','):
      if ':' not in rule:
        yield from process_range(rule, workflows, part_range)
      else:
        cond, workflow = rule.split(':')
        matching, part_range = part_range.split(cond)
        yield from process_range(workflow, workflows, matching)

class PartRange(NamedTuple):
  x: Tuple[int, int] = (1, 4001)
  m: Tuple[int, int] = (1, 4001)
  a: Tuple[int, int] = (1, 4001)
  s: Tuple[int, int] = (1, 4001)
  
  def split(self, rule):
    rating, comp, n = re.match(r'([xmas])([<>])(-?\d+)', rule).groups()
    n = int(n)
    r = getattr(self, rating)
    if comp == '>':
      return (
        self._replace(**{rating: (max(r[0], n+1), r[1])}),
        self._replace(**{rating: (r[0], n+1)})
      )
    elif comp == '<':
      return (
        self._replace(**{rating: (r[0], min(n, r[1]))}),
        self._replace(**{rating: (n, r[1])})
      )
  
  def combinations(self):
    count = lambda a,b: (b - a)
    return reduce(op.mul, (count(a, b) for a,b in self))

  def __bool__(self):
    valid = lambda a, b: a < b
    return all(valid(a,b) for a,b in self)

  def __iter__(self):
    yield from [self.x, self.m, self.a, self.s]

raw = '''
px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}
'''.strip('\n')

if __name__ == '__main__':
  sample = to_data(raw)
  for ans in main(sample, raw):
    print(ans)
