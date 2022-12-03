import json
import requests
import io
from pprint import pprint
from datetime import datetime
from csv import DictWriter
from subprocess import run, PIPE
from sys import stderr

# data/sessions.py: leaderboards = { '...': ['...'] }
from data.sessions import sessions, leaderboards

today = datetime.today()
days = datetime.today().day
url = 'https://adventofcode.com/{}/leaderboard/private/view/{}.json'

for session in sessions:
    for lid in leaderboards[session]:
      response = requests.get(url.format(today.year, lid), cookies={'session': session})
      data = json.loads(response.text)
      # extract completion times for each player
      # index: 2i + j = time for day i+1 puzzle j+1
      players = {
        m['name'] or m['id']: [
          m['completion_day_level']
          .get(str(i+1), {})
          .get(str(j+1), {})
          .get('get_star_ts')
          for i in range(days)
          for j in range(2)
        ]
        for m in sorted(
          data['members'].values(),
          key=lambda m: m['local_score'],
          reverse=True
        )
      }

      # pivot main axis to puzzles and sort each puzzle by time
      puzzles = {
        f'{i+1}.{j+1}':
        sorted([(name,ct) for name,t in players.items() if (ct := t[2*i+j]) != None], key=lambda nt: nt[1])
        for i in range(days)
        for j in range(2)
      }

      # calculate rank and score = #player - rank
      ranking = {p:data for p,pd in puzzles.items() if (data := {name:len(players)-i for i,(name,t) in enumerate(pd)})}
      ranking['total'] = {name: sum(p.get(name, 0) for p in ranking.values()) for name in players.keys()}

      # group by player
      header = ['Players'] + list(ranking.keys())
      data = [
        {'Players': player} | {
          puzzle:scores.get(player)
          for puzzle,scores in ranking.items()
          if player in scores
        } for player in players
      ]

      buf = io.StringIO()
      writer = DictWriter(buf, fieldnames=header)
      writer.writeheader()
      writer.writerows(data)
      csv = buf.getvalue()


      if run(['which', 'pandoc'], stdout=PIPE).returncode:
        print('Install pandoc for better output', file=stderr)
        print(csv)
      else:
        child = run(['pandoc', '-f', 'csv', '-t', 'markdown'], input=csv, text=True)
        child.check_returncode()
        print()
