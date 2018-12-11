#!/usr/bin/env python3

import sqlite3
import sys
import re

from collections import Counter
from ast import literal_eval

def main(args):
  db_path = args[0]
  conn = sqlite3.connect(db_path)
  cursor = conn.cursor()
  cursor.execute("SELECT role FROM participant WHERE role NOT NULL")
  roles = [v[0] for v in cursor.fetchall() if not v[0]=="test"]
  count = Counter()

#  sub = {
#    'anim': 'animator',
#    'art' : 'artist',
#    'cinematic' : 'cinematics',
#  }
#
#  for r in roles:
#    #for w in "artist animator senior manage admin lead".split():
#    r = r.split('(')[0]
#    for w in r.split():
#      w = sub.get(w,w)
#      if w == "/":
#        continue
#      count[w] += 1
#  for c, v in count.most_common():
#    print("{}: {}".format(c,v))
#
#  roles = sorted([r.split('(')[0].strip() for r in roles])
#  print(', '.join(roles))
#
#
#  cursor.execute("SELECT * FROM participant WHERE role NOT NULL")
#  for c in cursor.fetchall():
#    print(c)

  cursor.execute("""
    SELECT question.title, answer.answer FROM question
      JOIN survey ON survey.id = question.id_survey
      JOIN answer ON id_question = question.id
      JOIN participant ON participant.id = answer.id_participant
      WHERE question.title LIKE '%short description%'
  """)


  sub = {
    'tasks': 'task',
    'shot-task': 'task',
    'finding': 'find',
    'lookup': 'find',
    'searches': 'find',
    'search': 'find',
    'check': 'find',
    'feedback': 'information',
    'status': 'information',
    'update': 'information',
    'communicate': 'information',
  }

  count = Counter()
  set_ans = set()
  ans = cursor.fetchall()
  title = ans[0][0]
  for c in ans:
    if len(re.findall('test', c[1])) >= 3:
      continue
    set_ans.add(c[1])
#  print(title)
  dicts = [literal_eval(string) for string in set_ans]
  empty = 0
#  print()
  for d in dicts:
    for i, ans in d.items():
      for w in ans.split():
        w = w.lower()
        w = sub.get(w,w)
        count[w] += 1
      if not ans.strip():
        empty += 1
      else:
        pass
#        print(ans)
#  print()
#  print("{}/{}".format(empty, 3*len(dicts)))

  for w in "for to a on of and the i have".split():
    if count.get(w):
      del count[w]

  for k,v in count.most_common(20):
    print("{}:{}".format(k,v))

  dict_rev = {}
  for k,v in sub.items():
    l = dict_rev.get(v)
    if not l:
      l = dict_rev[v] = set()
    l.add(k)

#  for k,v in dict_rev.items():
#    print("\\begin{{minipage}}[c]{{{:.1f}\\textwidth}}".format(1.0/3.0))
#    print("\\begin{equation*} \\left. \\begin{tabular}{c}")
#    for w in v:
#      print("  \\text{{{}}} \\\\".format(w))
#    print("\\end{{tabular}}\\right \\}} \\text{{{}}} \\end{{equation*}}".format(k))
#    print("\\end{minipage}")
if __name__ == "__main__":
  main(sys.argv[1:])
