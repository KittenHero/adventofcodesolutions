from utils import *

@timing
def main(data, raw):
  survey = [row.split(' ')[0] for row in data if row]
  groups = [tuple(get_all_ints(row)) for row in data if row]
  yield sum(
    possible(row, group)
    for row, group in zip(survey, groups)
    if row
  )
  yield sum(
    possible('?'.join([row]*5), group*5)
    for row, group in zip(survey, groups)
    if row
  )

@lru_cache(maxsize=512)
def possible(row, expected, pos=0, count=0, validated=0):
  if pos == len(row):
    return (
      validated == len(expected) and not count
      or validated + 1 == len(expected) and count == expected[validated]
    )

  # too many '#'
  if (
    count and validated == len(expected)
    or validated < len(expected) and count > expected[validated]
  ):
    return 0

  def possible_damaged():
    return possible(row, expected, pos + 1, count + 1, validated)

  def possible_operational():
    if not count:
      return possible(row, expected, pos + 1, 0, validated)
    if count and count == expected[validated]:
      return possible(row, expected, pos + 1, 0, validated + 1)
    else:
      return 0

  if row[pos] == '#':
    return possible_damaged()
  if row[pos] == '.':
    return possible_operational()
  if row[pos] == '?':
    return possible_damaged() + possible_operational()

raw = '''
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
'''.strip('\n')

if __name__ == '__main__':
  sample = to_data(raw)
  for ans in main(sample, raw):
    print(ans)
