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

def read(name):
  with open(name) as f:
    return [l.strip() for l in f.readlines()]

def to_data(txt):
  return [l.strip() for l in txt.split('\n')]

def get_todays_input(session):
  today = datetime.now()
  url = f'https://adventofcode.com/{today.year}/day/{today.day}/input'
  cache = f'data/{today.year}.{today.day}.{session[-3:]}.input'
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

def submit_todays_answer(session, level, answer):
    today = datetime.now()
    url = f'https://adventofcode.com/{today.year}/day/{today.day}/answer'

    data = { 'level': level, 'answer': answer }
    response = requests.post(url, data, cookies={'session': session})
    root = BeautifulSoup(response.text, 'html.parser')
    print(root.find('main').text.strip())

# data/sessions.py: sessions = ['...']
from data.sessions import sessions
