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


def figure_progress(length, name, labels_x=[]):

  fig_height = 0.7 if labels_x else 0.3
  f = plt.figure(figsize=(0.5*length,fig_height))

  plt.scatter(range(length),[0]*length, c="grey")
  plt.yticks([],[])
  plt.xticks([],[])
  if labels_x:
    plt.xticks(range(len(labels_x)), labels_x, rotation=90)

  path_fig = os.path.join(cfg.PATH_DIR_FIGURES, "{}.pdf".format(name))
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


append("\\textbf{O:} Improve communication on how the project is going.")
append("\\begin{adjustwidth}{0.3cm}{}")
append("\\textbf{KR:} Email expanded draft each Monday for 10 weeks.")
append("\\includegraphics{{{}}}".format(path_fig_mondays))
append("\\textbf{KR:} 3 meetings/presentations with LTH supervisor before March.")
append("\\includegraphics{{{}}}".format(path_fig_3_meet_LTH))
append("\\textbf{KR:} 3 meetings/presentations with MASSIVE contacts before March.")
append("\\includegraphics{{{}}}".format(path_fig_3_meet_MASSIVE))
append("\\end{adjustwidth}")

print(os.linesep.join(
  [l if (l == out[-1] or (l.endswith('}') and ("begin{" in l or "end" in l)))
   else l+'\\\\' for l in out]))
