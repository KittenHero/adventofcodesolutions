from utils import *

def find_all(data, item):
  for y, row in enumerate(data):
    for x, char in enumerate(row):
      if char == item:
        yield x, y

def main(data, raw):
  s = next(find_all(data, 'S'))
  yield search(data, s)
  yield min(search(data, pos) for pos in chain([s], find_all(data, 'a')))

def search(data, start):
  visited = set()
  q = deque([(0, start, 0)])
  while q:
    steps, (x, y), prev  = q.popleft()
    if x < 0 or y < 0 or x >= len(data[0]) or y >= len(data) or (x,y) in visited:
      continue
    current = data[y][x]
    current = ord(current) - ord('a') if 'a' <= current <= 'z' else {'E': 26, 'S': 0}[current]
    if current > prev + 1:
      continue
    
    if current == 26:
      return steps
    visited.add((x,y))
    for dx, dy in [(0,1), (1,0), (-1, 0), (0, -1)]:
      q.append((steps + 1, (x + dx, y + dy), current))
  return float('inf')

if __name__ == '__main__':
  raw = '''
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
'''.strip('\n')

  sample = to_data(raw)
  for ans in main(sample, raw):
    print(ans)
