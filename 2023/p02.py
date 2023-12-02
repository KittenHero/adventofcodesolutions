from utils import *

def game_id(gid):
  return int(gid.split(' ')[1])

def count_color(value):
  count, color = value.split(' ')
  return Counter({color: int(count)})

def merge_colors(game):
  return reduce(lambda a,b: a|b, (
    count_color(color)
    for peek in game.split('; ')
    for color in peek.split(', ')
  ))

@timing
def main(data, raw):
  games = {
    game_id(game[0]): merge_colors(game[1])
    for line in data
    if line and (game := line.split(': '))
  }
  has =  Counter({'red': 12, 'green': 13, 'blue': 14})
  yield sum(gid for gid, seen in games.items() if seen <= has)
  yield sum(seen['red'] * seen['green'] * seen['blue'] for seen in games.values())

raw = '''
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
'''.strip('\n')

if __name__ == '__main__':
  sample = to_data(raw)
  for ans in main(sample, raw):
    print(ans)
