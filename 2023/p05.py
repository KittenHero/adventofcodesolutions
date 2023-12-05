from utils import *
import bisect

class RangeMap(NamedTuple):
  dst: int
  src: int
  r: int

  @property
  def src_end(self):
    return self.src + self.r
  
  @property
  def dst_end(self):
    return self.dst + self.r

  def map(self, src):
    return src + (self.dst - self.src) * (self.src <= src < self.src_end)

def location(seed, maps):
  for section in maps:
    # find le
    i = bisect.bisect_right([m.src for m in section], seed)
    if not i: continue
    m = section[i-1]
    seed = m.map(seed)
  return seed

def map_ranges(ranges, maps):
  for section in maps:
    mapped = []
    search = [m.src for m in section]
    for src, end in ranges:
      mapped.append((src, end))
      for m in section:
        # can go sequentially since each map is sorted
        src, end = mapped.pop()
        # |.a.| {.b.}
        if m.src_end <= src:
          mapped.append((src, end))
        # |.a.{-b-}.|
        elif m.src <= src < end <= m.src_end:
          mapped.append((m.map(src), m.map(end)))
        # |.a.{-b-|.}
        elif m.src <= src < m.src_end < end:
          mapped.append((m.map(src), m.dst_end))
          mapped.append((m.src_end, end))
        # {.b.|-a-|.}
        elif src < m.src < m.src_end < end:
          mapped.append((src, m.src))
          mapped.append((m.dst, m.dst_end))
          mapped.append((m.src_end, end))
        # {.b.|-a-}.|
        elif src < m.src < end < m.src_end:
          mapped.append((src, m.src))
          mapped.append((m.dst, m.map(end)))
        # {.b.} |.a.|
        elif end <= m.src:
          mapped.append((src, end))
    ranges = mapped
  return ranges

@timing
def main(data, raw):
  [seeds], *maps = [section.split(':')[1].split('\n') for section in raw.split('\n\n')]
  maps = [
    sorted(
      [
        RangeMap(*get_all_ints(line))
        for line in section
        if line
      ],
      key=lambda m: m.src
    )
    for section in maps
  ]
  seeds = get_all_ints(seeds)
  yield min(location(seed, maps) for seed in seeds)
  yield min(map_ranges(
    [(start, start + size)  for start, size in zip(seeds[::2], seeds[1::2])],
    maps
  ))[0]

raw = '''
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
'''.strip('\n')

if __name__ == '__main__':
  sample = to_data(raw)
  for ans in main(sample, raw):
    print(ans)
