from utils import *
from script import main
import importlib
import time
from argparse import ArgumentParser
import sys

if __name__ == '__main__':
  parser = ArgumentParser(description='Advent of Code Submission')
  parser.add_argument('--year', '-y', default=today.year, type=int)
  parser.add_argument('--dry-run', '--no-submit', '-n', action='store_true')
  group = parser.add_mutually_exclusive_group()
  group.add_argument('--day', '-d', default=today.day, type=int)
  group.add_argument('--solution', '-s', type=int)
  args = parser.parse_args()
  if args.solution:
    args.day = args.solution
    args.dry_run = True
    m = importlib.import_module(f'{args.year}.p{args.day:02}')
    main = m.main

  for session in sessions:
    raw = get_todays_input(session, day=args.day, year=args.year).strip()
    data = to_data(raw)
    start = time.process_time_ns()
    ans = list(main(data, raw))
    end = time.process_time_ns()
    print(f'{ans = }')
    print(f'elapsed: {(end - start) * 1e-9:.2f} CPU sec')
    if not args.dry_run:
      submit_todays_answer(session, len(ans), ans[-1], day=args.day, year=args.year)
