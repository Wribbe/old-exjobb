#!/usr/bin/env python3

import sys
import os
import sqlite3

from ast import literal_eval
from collections import Counter

# Assume we are running from the top-dir.
sys.path.insert(0, ".")
import config as cfg

conn = sqlite3.connect(cfg.PATH_DATABASE)

c = conn.execute("""
  SELECT
    answer.id,
    answer.id_participant,
    answer.answer,
    participant.name,
    question.data,
    question.title
  FROM question
    JOIN answer ON answer.id_question = question.id
    JOIN participant ON answer.id_participant = participant.id
  WHERE title LIKE "%reflect your%"
""")

cs = c.fetchall()
title = cs[0][-1]
words = literal_eval(cs[0][4])['words']
filtered = {}
for ans in sorted(cs):
  filtered[ans[1]] = literal_eval(ans[2])

count = Counter()
for idnum, data in filtered.items():
  for word in data:
    count[word] += 1

plot_type = "dots"

labels = []
labels_y = []

x = []
y = []

for i,k in enumerate([w.replace(',','').strip() for w in words.split()]):
  v = count.get(k,0)
  x += [i]*v
  y += range(v)
  labels.append(k)
  labels_y.append(i+1)

label_pos = range(len(labels))

#rotation_label=90
size=(2.7,2.2)

labels_pos_y = range(10)

rotate_figure=True
