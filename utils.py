from typing import *
from collections import *
from datetime import *
from itertools import *
from functools import *
import re
import operator as op
import heapq
from pprint import pprint
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from dataclasses import dataclass
import copy
import math

today = datetime.now()

def read(name):
  with open(name) as f:
    return [l.strip() for l in f.readlines()]

def to_data(txt):
  return [l.strip() for l in txt.split('\n')]

def get_todays_input(session, year=0, day=0):
  year = year or today.year
  day = day or today.day
  url = f'https://adventofcode.com/{year}/day/{day}/input'
  cache = f'data/{year}.{day}.{session[-3:]}.input'
  try:
    with open(cache, 'r') as f:
      return f.read()
  except FileNotFoundError:
    response = requests.get(url, cookies={'session': session})
    with open(cache, 'w') as f:
      f.write(response.text)
    return response.text

def get_all_ints(line):
  return [int(x) for x in re.findall('-?\d+', line)]

def submit_todays_answer(session, level, answer, year=0, day=0):
  year = year or today.year
  day = day or today.day
  url = f'https://adventofcode.com/{year}/day/{day}/answer'
  data = { 'level': level, 'answer': answer }
  response = requests.post(url, data, cookies={'session': session})
  root = BeautifulSoup(response.text, 'html.parser')
  print(root.find('main').text.strip())

@singledispatch
def print_grid(grid: dict):
  startx = min(x for x, y in grid)
  starty = min(y for x, y in grid)
  stopx = 1 + max(x for x, y in grid)
  stopy = 1 + max(y for x, y in grid)

  print('\n'.join(''.join(grid.get((x, y), '.') for x in range(startx, stopx)) for y in range(starty, stopy)))

@print_grid.register
def print_grid_list(grid: list):
  print('\n'.join(''.join(cell for cell in row) for row in range(grid)))

ops = {
  '+': op.add,
  '*': op.mul,
  '-': op.sub,
  '/': op.truediv,
}

# data/sessions.py: sessions = ['...']
from data.sessions import sessions
