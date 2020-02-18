from fuzzywuzzy import fuzz
from fuzzywuzzy import process

import csv

csvfile="lottery.csv"
with open(csvfile, newline='') as c:
  r=list(csv.DictReader(c))

names = [ l["first_name"] + " " + l["last_name"] for l in r ]


while len(names) > 0:
  name = names.pop()
  matches = process.extract(name, names, limit=5)
  matches = [ m for m in matches if m[1] > 90 ]
  if len(matches) > 0:
    print(name)
    print(matches)
