from utils import *

def main(data, raw, targety=2_000_000, bounds=4_000_000):
  sensors = []
  beacons = []

  for line in data:
    sx, sy, bx, by = map(int, re.findall('-?\d+', line))
    dist = abs(sx - bx) + abs(sy - by)
    sensors.append((sx, sy, dist))
    beacons.append((bx, by))

  yield sum(r - l - sum(y == targety and l <= x <= r for x,y in beacons) for l,r in row_coverage(sensors, targety))

  for y in range(bounds + 1):
    ranges = row_coverage(sensors, y)
    for (_, x), _ in zip(ranges, ranges[1:]):
      if 0 <= x <= bounds:
        yield y + x*4_000_000
        return

def row_coverage(sensors, targety):
  # [start, stop)
  ranges = sorted([
    (x - sx_range, x + sx_range + 1)
    for x, y, s_range in sensors
    if (sx_range := s_range - abs(targety - y)) >= 0
  ])
  if not ranges:
    return []

  merged = []
  mleft, mright = ranges[0]
  for l, r in ranges[1:]:
    assert mleft <= l <= r, f'{mleft=},{l=},{r=}'
    if mright < l:
      merged.append((mleft, mright))
      mleft = l
      mright = r
    else:
      mright = max(r, mright)
  else:
    merged.append((mleft, mright))
  assert all(right < left for (_, right), (left, _) in zip(merged, merged[1:]))
  return merged

if __name__ == '__main__':
  raw = '''
Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3
'''.strip('\n')

  sample = to_data(raw)
  for ans in main(sample, raw, targety=10, bounds=20):
    print(ans)
