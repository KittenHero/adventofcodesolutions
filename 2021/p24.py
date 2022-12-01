from utils import *


N_DIGITS = 14
DIGITS = list(range(1,10))

a = [0]*N_DIGITS
b = [0]*N_DIGITS
c = [0]*N_DIGITS

for i in range(N_DIGITS):
    section = data[i*18:(i+1)*18]
    a[i] = int(section[5].split()[-1])
    b[i] = int(section[4].split()[-1])
    c[i] = int(section[15].split()[-1])

def block(i, z, w):
    x = a[i] + (z % 26)
    z //= b[i]
    z += (x!=w)*(w + c[i] + 25*z)
    return z

max_z = [reduce(mul, b[i:]) for i in range(N_DIGITS)]

def help_solve(i, z):
    if i == N_DIGITS and not z:
        return [0]
    elif i < N_DIGITS and z < max_z[i]:
        return solve(i, z)
    else:
        return []

@cache
def solve(i, z):
    opts = DIGITS
    return [
        w*(10**(N_DIGITS-i-1)) + s
        for w in opts
        for s in help_solve(i+1, block(i, z, w))
    ]

lowest, *_, highest = solve(0, 0)
print(highest)
print(lowest)
