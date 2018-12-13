#!/usr/bin/env python3

import sys
sys.path.append(".")

import re
import os

import config as cfg
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime as dt
from datetime import timedelta as td

out = []

def append(text):
  out.append(text)

def add(text):
  out[-1] += text

#data = np.random.randint(0,12,size=72)
#bins = np.arange(13)-0.5

#hist, edges = np.histogram(data, bins=bins)
#y = np.arange(1,hist.max()+1)
#x = np.arange(12)
#X,Y = np.meshgrid(x,y)

mark_checked = "$\u2713$"
mark_not_checked = "$\u2610$"

def figure_progress(length, name, labels_x=[]):

  fig_height = 0.67 if labels_x else 0.2
  if length == 1:
    figsize = (0.2, fig_height)
  else:
    figsize = (0.5*length,fig_height)
  f = plt.figure(figsize=figsize)

  plt.scatter(range(length),[0]*length, marker=mark_not_checked)
  plt.yticks([],[])
  plt.xticks([],[])

  path_fig = os.path.join(cfg.PATH_DIR_FIGURES, "{}.pdf".format(name))
  if labels_x:
    plt.xticks(range(len(labels_x)), labels_x, rotation=90)
  if not os.path.isdir(os.path.dirname(path_fig)):
    os.makedirs(os.path.dirname(path_fig))
  plt.tight_layout(pad=0)
  f.savefig(path_fig)
  return path_fig

date_start = dt.strptime("2018-12-13", "%Y-%m-%d")
fmt_month = "%d/%m"
mondays = [date_start + td(days=x) for x in
           range(10*7+1) if (date_start+td(days=x)).weekday() == 0]
labels_mondays = [dt.strftime(d, fmt_month) for d in mondays]

path_fig_mondays = figure_progress(10, "draft_mondays", labels_mondays)
path_fig_3_meet_LTH = figure_progress(3, "meet_lth")
path_fig_3_meet_MASSIVE = figure_progress(3, "meet_massive")

def label_month(d):
  return dt.strftime(d, fmt_month)

def label_weekday(d):
  return dt.strftime(d, "%A")

def label_weekdate(d):
  return "{} {}".format(label_weekday(d), label_iso(d))

def label_iso(d):
  return dt.strftime(d, "%Y-%m-%d")

day_last_draft = mondays[-1]+td(days=4)

count_O = -1
conut_KR = -1
def objective(text):
  global count_KR; global count_O;
  count_KR = 0
  count_O += 1
  fmt_object ="\\textbf{{O{}: {}}}"
  if count_O > 0:
    append("\\end{adjustwidth}")
  append(fmt_object.format(count_O, text))
#  append("\\vspace{-0.4cm}")
  append("\\begin{adjustwidth}{0.3cm}{}")

def keyresult(text, image):
  global count_KR
  fmt_kr = "\\textbf{{KR{}.{}:}} \\\\ {}"
  count_KR += 1
  append(fmt_kr.format(count_O, count_KR, text))
  append("\\vspace{-0.3cm}")
  append("\\begin{center}")
  append("\\includegraphics")
  add("{{{}}}".format(image))
  append("\\end{center}")

fmt_in_person = "Make three in-person presentations of current work and direction at {} \
  before {} {}.".format("{}", label_weekday(day_last_draft),
                        label_month(day_last_draft))

days_allotted = 7*12+1
day_finished = date_start + td(days=days_allotted)

append("\\newgeometry{top=1cm, bottom=1cm}")
append("\\section{OKR's (\\today)}")
append("\\vspace{-1.2cm}")

objective(
  "Complete all diploma-work on my side no later than {} {}.".format(
  label_weekday(day_finished), label_iso(day_finished)))
keyresult("Send in final report draft no later than {}.".format(
  label_weekdate(day_finished-td(days=7))),
  figure_progress(1,"final_draft"))
keyresult("Opposition on other master thesis done no later than {}.".format(
  label_weekdate(day_finished-td(days=7*2))),
  figure_progress(1,"opposition_done"))

objective("Improve communication on how the project is going.")
keyresult("Email expanded draft each Monday for 10 weeks.", path_fig_mondays)
keyresult(fmt_in_person.format("LTH"), path_fig_3_meet_LTH)
keyresult(fmt_in_person.format("MASSIVE"), path_fig_3_meet_MASSIVE)
#append("\\includegraphics{{{}}}".format(path_fig_3_meet_LTH))
#append("\\textbf{KR0.3:} 3 meetings/presentations with MASSIVE contacts before March.")
#append("\\includegraphics{{{}}}".format(path_fig_3_meet_MASSIVE))
#

do_end = [
  "includegraphics"
]


append("\\end{adjustwidth}")
append("\\restoregeometry")
print(os.linesep.join(
  [l if (l == out[-1] or (l.endswith('}') and not (any([v in l for v in do_end]))))
   else l+'\\\\' for l in out]))
