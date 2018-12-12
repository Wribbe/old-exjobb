import sys
sys.path.insert(0, ".")
import os
import random


import sqlite3
import config as cfg
import re

from ast import literal_eval
from collections import Counter

conn = sqlite3.connect(cfg.PATH_DATABASE)
c = conn.execute("""
  SELECT
    answer.id,
    participant.id,
    participant.name,
    answer.answer
  FROM question
    JOIN answer ON answer.id_question = question.id
    JOIN participant ON participant.id = answer.id_participant
  WHERE question.title LIKE "%related functionalities that would%"
""")

cs = c.fetchall()
filtered = {}
for id_a, id_p, name_p, ans in cs:
  if int(id_p) == 1:
    continue
  filtered[id_p] = literal_eval(ans)

suggestions = []
for id_p in sorted(filtered):
  d = filtered[id_p]
  suggestions += [v.strip() for v in d.values() if v.strip()]

def sanitize_word(word):
  return re.sub(r'\W','', word.strip().lower())

def sanitize_words(words):
  return [w for w in [sanitize_word(w) for w in words] if w.strip()]

words = []
for line in suggestions:
  words += sanitize_words(line.split())

ignore = "of to a and the for in that with it if wold were when i".split()

sub = {
  'tasks': 'task',
}


class search_window:

  def __init__(self):
    self.snippets=[]

  def check(self, word, words, num_words):
    for i, w in enumerate(words):
      w = sub.get(w,w)
      if w == word:
        first = max(0, i-num_words)
        last = min(len(words), i+num_words+1)
        self.snippets.append(' '.join(words[first:last]))

  def __str__(self):
    return os.linesep.join(self.snippets)


count = Counter()
for w in words:
  if w in ignore or not w.strip():
    continue
  count[w] += 1

ignore_action = """\
all
are
set
for
and
there
so
that
of
they
with
many
my
more
if
the
is
to
on
in
its
add
sort
much
per
a
just
too
an
like
it
as
""".split()


sub_categories = {
  'automation': [
    'autofills',
    'autoupload',
    'automatic',
    'parent',
    'batch',
  ],
  'presentation': [
    'information',
    'cluttered',
    'info',
    'reference',
    'tags',
    'clearer',
    'organized',
    'clearly',
    'correctly',
    'graphing',
    'images',
  ],
  'enforcement': [
    'forcing',
    'need',
    'differently',
  ],
  'communication': [
    'available',
    'spammed',
    'email',
    'leads',
    'lead',
    'feedback',
    'review'
  ],
  'usability': [
    'navigation',
    'uploader',
    'integration',
    'integrated',
    'integrations',
    'management',
    'flows',
    'flow',
    'fewer',
    'versions',
  ],
  'functionality': [
    'storing',
    'kanban',
    'planning',
  ],


}

class categoryCounter():

  def __init__(self, dict_sub):
    self.values = {}
    self.reversed_sub = {}
    for key in dict_sub:
      self.values[key] = 0
    for key, values in dict_sub.items():
      for v in values:
        if not v:
          continue
        self.reversed_sub[v] = key

  def count(self, word_set):
    for word in word_set:
      cat = self.reversed_sub.get(word)
      if cat:
        self.values[cat] += 1

  def __str__(self):
    return str(self.values)


action_lines = []
for line in suggestions:
  action_lines.append(sanitize_words(line.split()))

lines_non_action_ignored = []
for line in action_lines:
  lines_non_action_ignored.append([w for w in line if w not in ignore_action])

#task_window = search_window()
#for word_set in action_lines:
#  word_set = [w for w in word_set if w not in ignore_action]
#  task_window.check('task', word_set, 4)
##print(task_window)
##print("")
#
#task_window = search_window()
#for word_set in action_lines:
#  word_set = [w for w in word_set if w not in ignore_action]
#  task_window.check('better', word_set, 4)
##print(task_window)
##print("")

cat_count = categoryCounter(sub_categories)
for line in lines_non_action_ignored:
#  print(' '.join(line))
  cat_count.count(line)
#print()
#print(cat_count)

colors = """Apricot Aquamarine Bittersweet Black Blue BlueGreen BlueViolet
BrickRed Brown BurntOrange CadetBlue CarnationPink Cerulean CornflowerBlue Cyan
Dandelion DarkOrchid Emerald ForestGreen Fuchsia Goldenrod Gray Green
GreenYellow JungleGreen Lavender LimeGreen Magenta Mahogany Maroon Melon
MidnightBlue Mulberry NavyBlue OliveGreen Orange OrangeRed Orchid Peach
Periwinkle PineGreen Plum ProcessBlue Purple RawSienna Red RedOrange RedViolet
Rhodamine RoyalBlue RoyalPurple RubineRed Salmon SeaGreen Sepia SkyBlue
SpringGreen Tan TealBlue Thistle Turquoise Violet VioletRed WildStrawberry
Yellow YellowGreen YellowOrange""".split()

path_categories = os.path.join(cfg.PATH_DIR_TEX, 'report', 'survey001_Q4_categories.tex')
out = []
cols = ["MidnightBlue", "Fuchsia", "ForestGreen", "BurntOrange", "Aquamarine",
        "BrickRed"]
for i, (category,color) in enumerate(zip(sorted(sub_categories), cols)):
  out.append("\\begin{minipage}[b]{0.32\\textwidth}")
  out.append("\\begin{equation*}")
  out.append("  \\left. \\begin{tabular}{c}")
  for s in sub_categories[category]:
    out.append("    \\text{{{}}} \\\\".format(s))
  out.append("  \\end{tabular} \\hspace{-0.2cm} \\right \}")
#  category = "\\textcolor{{{}}}{{{}}}".format(color, category)
  category = "{}".format(category.title())
  if not i == len(sub_categories)-1:
    out.append("  \\text{{{},}}".format(category))
  else:
    out.append("  \\text{{{}}}".format(category))
  out.append("\\end{equation*}")
  out.append("\\end{minipage}")

with open(path_categories, 'w') as handle_file:
  handle_file.write(os.linesep.join(out))
  handle_file.write(os.linesep)


#print(count.most_common())

def invert_sub(sub_dict):
  ret = {}
  for k,vs in sub_dict.items():
    for v in vs:
      ret[v] = k
  return ret

def colorize_line(colors, categories, line):
  out = []
  col_dict = {cat : (i, col) for i,(cat,col) in enumerate(zip(categories,colors), start=1)}
  cats_inverted = invert_sub(categories)
  for word in line.split():
    t = col_dict.get(cats_inverted.get(sanitize_word(word), None), None)
    if t:
      i, color = t
      out.append("\\textcolor{{{}}}{{$\\textbf{{\\text{{{}}}}}^{{{}}}$}}".format(color, word, i))
    else:
      out.append(word)
  return ' '.join(out)


path_ans_out = os.path.join(cfg.PATH_DIR_TEX, 'report', 'survey001_Q4_ans.txt')
#if not os.path.isfile(path_ans_out):
suggestions = [colorize_line(cols, sub_categories, line) for line in suggestions]
heading = ["\\\\ Category legend:"]
categories = ["\\textcolor{{{}}}{{$\\text{{{}}}^{{{}}}$}}".format(c,cat.title(),i) for i,(c
           ,cat) in enumerate(zip(cols, sub_categories), start=1)]
legend = heading + [', '.join(categories)+'.'] + ["\\\\"]
suggestions = [' '.join(legend)] + suggestions
with open(path_ans_out, 'w') as handle_f:
  handle_f.write("\\\\{}".format(os.linesep).join(suggestions))
  handle_f.write(os.linesep)

revsorted = lambda l: reversed(sorted(l))

plot_type="dots"
maxy = range(max(cat_count.values.values()))
x = []
y = []
for i, (category, value) in enumerate(revsorted(cat_count.values.items())):
  x += [i] * value
  y += range(value)

label_pos = range(len(cat_count.values.keys()))
labels_pos_y = maxy[0::3]
labels_y = [1+v for v in maxy[0::3]]
labels = [l.title() for l in revsorted(cat_count.values.keys())]

#rotation_label=90
rotate_figure = True
