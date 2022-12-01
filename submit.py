from utils import *
from script import main

for session in sessions:
  raw = get_todays_input(session)
  data = to_data(raw)
  ans = list(main(data, raw))
  submit_todays_answer(session, len(ans), ans[-1])
