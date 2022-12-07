from utils import *

class Dir:
  def __init__(self, parent=None):
    self.parent = parent
    self.files = {}
    self.dirs = {}
  
  @lru_cache
  def __len__(self):
    return sum(self.files.values()) + sum(len(dir) for dir in self.dirs.values())

def main(data, raw):
  root = Dir()
  current = root
  all_dirs = []
  for line in ['$ ls', 'dir /'] + data:
    match line.split(' '):
      case ['$', 'cd', '..']:
        current = current.parent
      case  ['$', 'cd', dir]:
        current = current.dirs[dir]
      case ['$', 'ls']:
        all_dirs.append(current)
      case ['dir', name]:
        current.dirs[name] = Dir(parent=current)
      case [size, name] if size.isdigit():
        current.files[name] = int(size)
  
  yield sum(size for d in all_dirs if (size := len(d)) <= 100000)
  total_space = 70000000
  required_space = 30000000
  used_space = len(root)
  yield min(size for d in all_dirs if used_space - (size := len(d)) + required_space <= total_space)

if __name__ == '__main__':
  raw = '''
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
'''.strip('\n')

  sample = to_data(raw)
  for ans in main(sample, raw):
    print(ans)
