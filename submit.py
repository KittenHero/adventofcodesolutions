from utils import *
from script import main

for session in sessions:
  raw = get_todays_input(session).strip()
  data = to_data(raw)
  ans = list(main(data, raw))
  print(f'{ans = }')
  submit_todays_answer(session, len(ans), ans[-1])
