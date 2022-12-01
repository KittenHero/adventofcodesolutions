from utils import *

scanners = []
for l in data:
    if l == '': continue
    if re.match('---.+---', l):
        scanners.append([])
    else:
        x,y,z = map(int, re.findall('-?\d+', l))
        scanners[-1] += [(x,y,z)]

def rotations():
    # ijk = 012
    for x,y,z in permutations(range(3)):
        for a,b in product([1, -1], repeat=2):
            # ixj=k jxk=i kxi=j jxi=-k kxj=-i ixk=-j
            cross = 2*((x + 1)%3 == y) - 1
            yield lambda p: (a*p[x], b*p[y], a*b*cross*p[z])

def offset(to,_from):
    a,b,c = to
    x,y,z = _from
    return (a-x,b-y,c-z)

def align(scanners, known, offsets):
    for i,s in enumerate(scanners):
        for ref_point, rel_point in product(known, s):
            for r in rotations():
                o = offset(r(rel_point), ref_point)
                ss = {offset(r(p), o) for p in s}
                if len(ss & known) < 12: continue
                known |= ss
                offsets += [o]
                scanners.pop(i)
                return

known = set(scanners.pop(0))
offsets = [(0,0,0)]
while scanners:
    align(scanners, known, offsets)
    print(f'\r|{"*"*len(offsets)}{" "*len(scanners)}|', end='')
print()

print(len(known))

def mdist(p,q):
    return sum(abs(c) for c in offset(p,q))

print(max(mdist(*pq) for pq in combinations(offsets, 2)))