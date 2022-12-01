from utils import *

rooms = {'A': 3, 'B':5, 'C':7,'D':9}
energy = {'A': 1, 'B':10, 'C':100, 'D': 1000}

def bstr(board):
    return '\n'.join(
        ''.join(c for c in row)
        for row in board
    )

def cost(t, ax,ay, bx, by):
    return energy[t]*(abs(ay-by) + abs(ax-bx)), ax,ay, bx,by

def valid_moves(board):
    hall = board[1]
    # move to hall
    for t,i in rooms.items():
        badroom = [(j, row[i]) for j,row in enumerate(board[2:-1],start=2) if row[i] != '.']
        if all(tt == t for j,tt in badroom): continue
        j, t = badroom[0]
        for k in range(i-1, 1, -2):
            if hall[k] != '.': break
            yield cost(t, i,j, k,1)
        else:
            if hall[1] == '.': yield cost(t, i,j, 1,1)
        for k in range(i+1, 11, 2):
            if hall[k] != '.': break
            yield cost(t, i,j, k,1)
        else:
            if hall[11] == '.': yield cost(t, i,j, 11,1)
    # move to correct room
    height = len(board)
    for i,t in enumerate(hall[1:-1], start=1):
        if t == '.': continue
        k = rooms[t]
        if any(row[k] not in [t, '.'] for row in board[2:-1]): continue
        low,hi = min(i,k), max(i,k)
        if any(h != '.' for h in hall[low+1:hi]): continue
        j = max(j for j in range(height) if board[j][k] == '.')
        yield cost(t, i,1, k,j)

def heuristic(board):
    h = 0
    good = {v:0 for v in 'ABCD.# '}
    roomh = len(board[2:-1])
    for j,row in enumerate(board[1:-1], 1):
        for i,t in enumerate(row[1:-1], 1):
            if t not in energy: continue
            if rooms[t] != i:
                h += energy[t]*(abs(i - rooms[t]) + j + good[t])
                good[t] += 1
    return h

def freeze(board):
    return tuple(tuple(r) for r in board)

def solve(board, target):
    target = freeze(target)
    q = [(0, 0, freeze(board))]
    visited = set()
    mc = 0
    while q:
        f, c, board = heapq.heappop(q)
        if board == target: return c
        if board in visited: continue
        visited.add(board)
        for cc,x,y,a,b in valid_moves(board):
            bb = [list(l) for l in board]
            bb[y][x], bb[b][a] = '.', bb[y][x]
            ff = c+cc+heuristic(bb)
            heapq.heappush(q, (ff, c+cc, freeze(bb)))

target = '''
#############
#...........#
###A#B#C#D###
  #A#B#C#D#
  #########
'''.strip().split('\n')

extra = '''
  #D#C#B#A#
  #D#B#A#C#
'''.strip('\n').split('\n')

print(solve(data, target))


data[3:3] += extra
target[3:3] += 2*[target[3]]
print(solve(data, target))
