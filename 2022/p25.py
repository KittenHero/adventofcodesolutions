from utils import *

digits = dict(zip('=-012', range(-2,3)))
inv_digits = {v: k for k, v in digits.items()}
max_digit = 2
inv_max_digit = inv_digits[max_digit]
base = 5

@timing
def main(data, raw):
  s = sum(
    digits[k]*base**i
    for line in data
    for i, k in enumerate(reversed(line))
  )
  snafu = []
  power = next(i for i in count() if max_digit * base ** i >= s)

  for i in range(power, -1, -1):
    def f(d):
      return digits[d] * base ** i
    def ss(d):
      return s - f(d)
    def key(d):
      return abs(ss(d))
    d = min(
      (
        k for k in digits
        if key(k) <= f(inv_max_digit)
      ),
      key=key
    )
    s = ss(d)
    snafu.append(d)

  yield ''.join(snafu)
  yield '[Start The Blender]'

raw = '''
1=-0-2
12111
2=0=
21
2=01
111
20012
112
1=-1=
1-12
12
1=
122
'''.strip('\n')

if __name__ == '__main__':
  sample = to_data(raw)
  for ans in main(sample, raw):
    print(ans)
