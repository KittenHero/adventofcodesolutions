from utils import *

@timing
def main(data, raw):
  sequence = data[0].split(',')
  yield sum(map(hash, sequence))
  yield focal_power(sequence)

def hash(str):
  v = 0
  for ch in str:
    v = (v + ord(ch))*17 & 0xff
  return v

def focal_power(sequence):
  library = [OrderedDict() for _ in range(256)]
  for ins in sequence:
    if '=' in ins:
      k, v = ins.split('=')
      library[hash(k)][k] = int(v)
    if '-' in ins:
      k = ins.strip('-')
      library[hash(k)].pop(k, 0)
  return sum(
    i * j * focal_length
    for i, box in enumerate(library, start=1)
    for j, focal_length in enumerate(box.values(), start=1)
  )

raw = '''
rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7
'''.strip('\n')

if __name__ == '__main__':
  sample = to_data(raw)
  for ans in main(sample, raw):
    print(ans)
