# Advent of Code Solutions & utility scripts

## requirements:
  [python3]
  beautifulsoup4
  requests

## usage:

Edit your solution in script.py and put example input in `raw`.  The `main` function should `yield` the answer for each part.

`> python script.py`

Create `data/sessions.py` and put your session cokies and private leaderboards in there:

```py
sessions = ['<cookie>']
leaderboards = {'<cookie': ['leaderboads id']}
```

Once you're sure you have the correct answer, submit your solution to today's problem using:

`> python submit.py`

or to submit to a previuos problem

`> python submit.py -d DD -y YYYY`

or to run a script from previous solutions:

`> python submit.py -s DD -y YYYY`

