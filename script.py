from utils import *


def main(data, raw):
    yield ...

if __name__ == '__main__':
  raw = '''
1000
2000
3000

4000

5000
6000

7000
8000
9000

10000
'''.strip()

  sample = to_data(raw)
  for ans in main(sample, raw):
    print(ans)
