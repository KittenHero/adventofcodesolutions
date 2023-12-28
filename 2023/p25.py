from utils import *
import random

@timing
def main(data, raw):
  graph = defaultdict(Counter)
  for row in data:
    if not row: continue
    src, *dst = row.replace(':', '').split(' ')
    i = frozenset({src})
    for d in dst:
      j = frozenset({d})
      graph[i][j] += 1
      graph[j][i] += 1

  # yield greedy_min_cut(graph, 3)
  random.seed(1234)
  while cut_degree(reduced := fast_min_cut(graph, 3)) != 3:
    continue
  yield reduce(op.mul, map(len, reduced.keys()))

def fast_min_cut(graph, k=1):
  '''Karger-Stein'''
  n = len(graph)
  if n <= 6:
    return contract(graph, 2)
  t = math.ceil(1 + n * 2**-0.5)
  g1 = fast_min_cut(contract(graph, t), k)
  c1 = cut_degree(g1)
  if c1 == k:
    return g1
  g2 = fast_min_cut(contract(graph, t), k)
  c2 = cut_degree(g2)
  return g1 if c1 < c2 else g2
  
def cut_degree(contracted_graph):
  s, t = contracted_graph
  return contracted_graph[s][t]

def contract(graph, k):
  graph = defaultdict(Counter, {s: Counter(dst) for s, dst in graph.items()})
  for _ in range(len(graph)-k):
    edges, weights = zip(*(((s, t), w) for s, e in graph.items() for t, w in e.items()))
    s, t = random.choices(edges, weights)[0]
    merge(graph, s, t)
  return graph

def greedy_min_cut(graph, k=1):
  '''Stoer-Wagner'''
  n = len(graph)
  for i in range(1, n):
    s = t = next(iter(graph))
    subset = s
    sub_edges = Counter(graph[s])
    for _ in range(n-i):
      subset |= t
      del sub_edges[t]
      s, t = t, max(sub_edges, key=lambda i: sub_edges[i])
      for e, w in graph[t].items():
        if e & subset: continue
        sub_edges[e] += w
    if sub_edges[t] == 3:
      m = len(subset)
      return m*(n-m)
    merge(graph, s, t)

def merge(graph, s, t):
  st = s | t
  del graph[s][t]
  del graph[t][s]
  for w in graph[s]:
    graph[st][w] += graph[s][w]
    graph[w][st] += graph[w][s]
    del graph[w][s]
  for w in graph[t]:
    graph[st][w] += graph[t][w]
    graph[w][st] += graph[w][t]
    del graph[w][t]
  del graph[s]
  del graph[t]

raw = '''
jqt: rhn xhk nvd
rsh: frs pzl lsr
xhk: hfx
cmg: qnr nvd lhk bvb
rhn: xhk bvb hfx
bvb: xhk hfx
pzl: lsr hfx nvd
qnr: nvd
ntq: jqt hfx bvb xhk
nvd: lhk
lsr: lhk
rzs: qnr cmg lsr rsh
frs: qnr lhk lsr
'''.strip('\n')

if __name__ == '__main__':
  sample = to_data(raw)
  for ans in main(sample, raw):
    print(ans)
