from utils import *

calibration_digits = r'\d|one|two|three|four|five|six|seven|eight|nine'

def unword(w):
  return str(
    calibration_digits.split('|').index(w)
  ) if w in calibration_digits else w

def calibration_value(matches):
  return int(unword(matches[0]) + unword(matches[-1]))

def calibration_sum(pattern, data):
  return sum(
    calibration_value(matches)
    for line in data
    if (matches := re.findall(pattern, line))
  )

@timing
def main(data, raw):
  yield calibration_sum(r'\d', data)
  # use look-ahead regex to not consume overlapping matches
  yield calibration_sum(f'(?=({calibration_digits}))', data)

raw = '''
two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
'''.strip('\n')

if __name__ == '__main__':
  sample = to_data(raw)
  for ans in main(sample, raw):
    print(ans)
