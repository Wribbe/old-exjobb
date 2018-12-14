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

def new_page():
  append("\\newpage")

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
    figsize = (min(0.5*length, 5.5),fig_height)
  f = plt.figure(figsize=figsize)

  plt.scatter(range(length),[0]*length, marker=mark_not_checked)
  plt.yticks([],[])
  plt.xticks([],[])

  plt.box(False)
  path_fig = os.path.join(cfg.PATH_DIR_FIGURES, "{}.pdf".format(name))
  if labels_x:
    plt.xticks(range(len(labels_x)), labels_x, rotation=90)
  if not os.path.isdir(os.path.dirname(path_fig)):
    os.makedirs(os.path.dirname(path_fig))
  plt.tight_layout(pad=0)
  f.savefig(path_fig)
  return path_fig

day_start = dt.strptime("2018-12-13", "%Y-%m-%d")
fmt_month = "%d/%m"
mondays = [day_start + td(days=x) for x in
           range(10*7+1) if (day_start+td(days=x)).weekday() == 0]
labels_mondays = [dt.strftime(d, fmt_month) for d in mondays]

path_fig_mondays = figure_progress(10, "draft_mondays", labels_mondays)

def label_month(d):
  return dt.strftime(d, fmt_month)

def label_weekday(d):
  return dt.strftime(d, "%A")

def label_weekdate(d):
  return "{} {}".format(label_weekday(d), label_iso(d))

def label_iso(d):
  return dt.strftime(d, "%Y-%m-%d")

day_last_draft = mondays[-1]+td(days=4)

count_O = 0
conut_KR = -1
def objective(text, date=None):
  global count_KR; global count_O;
  count_KR = 0
  count_O += 1
  fmt_object ="\\textbf{{\\mybox{{O{}:}} {}}}"
  if count_O > 1:
    append("\\end{adjustwidth}")
  if date:
    text = text.format(label_weekdate(date))
  append(fmt_object.format(count_O, text))
  append("\\vspace{0.2cm}")
  append("\\begin{adjustwidth}{0.3cm}{}")

def keyresult(text, image, date=None):
  global count_KR
  fmt_kr = "\\textbf{{KR{}.{}:}} \\\\ {}"
  count_KR += 1
  if date:
    text = text.format(label_weekdate(date))
  append(fmt_kr.format(count_O, count_KR, text))
#  append("\\vspace{0.3cm}")
  append("\\begin{center}")
  append("\\includegraphics")
  add("{{{}}}".format(image))
  append("\\end{center}")

def days_from_start(n):
  return day_start+td(days=n)

fmt_in_person = "Do three ten minutes in-person presentations of current work and direction at {} \
  before {}.".format("{}", label_weekdate(day_last_draft))

days_allotted = 7*12+1
day_finished = day_start + td(days=days_allotted)

day_last_draft_report = day_finished-td(days=7)
day_last_oposition = day_finished-td(days=7*2)
day_last_draft_presentation = day_finished-td(days=7+4)

append("\\newgeometry{top=1cm, bottom=1cm, footskip=0.0cm}")
append("\\section{Project OKRs (\\today) \\\\ \
       {\\normalsize (\\textbf{O}bjectives and \\textbf{K}ey \\textbf{R}esults)}}")
append("\\vspace{-1.2cm}")

objective(
  "Complete all diploma-work sans feedback no later than {}.",
  day_finished)
keyresult(
  "Send in final report draft no later than {}.",
  figure_progress(1,"final_draft"),
  day_last_draft_report)
keyresult(
  "Opposition on other master thesis done no later than {}.",
  figure_progress(1,"opposition_done"),
  day_last_oposition)
keyresult(
  "Final version of presentation done no later than {}.",
  figure_progress(1,"presentation_done"),
  day_last_draft_presentation)

objective("Improve communication on how the project is progressing.")
keyresult("Email expanded draft each Monday for 10 weeks.", path_fig_mondays)
keyresult(
  fmt_in_person.format("LTH", "{}"),
  figure_progress(3,"presentation_LTH"),
  day_last_draft_presentation)
keyresult(
  fmt_in_person.format("MASSIVE", "{}"),
  figure_progress(3,"presentation_MASSIVE"),
  day_last_draft_presentation)
keyresult("Finalize and email this OKR document no later than {}.".format(
  label_weekdate(days_from_start(1))),
  figure_progress(1,"finalize_OKRs"))

objective("Do opposition on interesting master thesis.")
keyresult("Find 8 promising thesis projects no later than {}.".format(
  label_weekdate(days_from_start(7))),
  figure_progress(8,"found_opposition_thesis"))
keyresult("Contact at least three students of the eight no later than {}.".format(
  label_weekdate(days_from_start(7+12+7))),
  figure_progress(3,"selected_opposition_thesis"))
keyresult("Final opposing thesis confirmed no later than {}.".format(
  label_weekdate(days_from_start(7+12+7*3))),
  figure_progress(1,"final_opposition_thesis"))


objective(
  "Ensure a robust grounding in scientific literature.")
keyresult(
  "Find and save at least 15 promising articles to reference, no later than {}.",
  figure_progress(15,"references_articles"),
  days_from_start(7+12+3))
keyresult(
  "Find at least 3 promising books to references, no later than {}.",
  figure_progress(3,"references_books"),
  days_from_start(7+12+3))
keyresult(
  "Argue for and get all references vetted by supervisor no later than {}.",
  figure_progress(1,"vet_references"),
  days_from_start(7+12+3+5))

new_page()

day_last_gathered_data = dt.strptime("2019-02-11", "%Y-%m-%d")

objective(
  "All data gathered no later than {}.",
  day_last_gathered_data)
keyresult(
  "Create personas no later than {}.",
  figure_progress(1,"create_personas"),
  day_start+td(days=5))
keyresult(
  "Send out 5 additional online surveys to the team no later than {}.",
  figure_progress(5,"additional_online_surveys"),
  day_last_gathered_data-td(days=7))
keyresult(
  "Complete 8 in-person interviews no later than {}.",
  figure_progress(8,"interviews"),
  day_last_gathered_data-td(days=3))
keyresult(
  "Perform 3 interface-theory tests with 3 participants each no later than {}.",
  figure_progress(9,"interface_tests"),
  day_last_gathered_data-td(days=5))

objective(
  "Usable integrated prototype with Shotgun no later than {}.",
  day_last_draft_presentation-td(days=7))
keyresult(
  "Confirm 3 user-changes in prototype affecting Shotgun no later than {}.",
  figure_progress(3,"shotgun_propagation"),
  day_last_gathered_data-td(days=7*3.0))
keyresult(
  "Finalize 3 tasks that should be functional in in prototype no later than {}.",
  figure_progress(3,"shotgun_tasks"),
  day_last_gathered_data-td(days=7*2.0))
keyresult(
  "Apply results of each theory tests to Shotgun prototype no later than. {}.",
  figure_progress(3,"interface_shotgun_tests"),
  day_last_gathered_data+td(days=7))

objective(
  "Figure out how to test interface-theory no later than {}.",
  day_start+td(days=7*2))

append("\\end{adjustwidth}")
append("\\restoregeometry")

do_end = [
  "includegraphics"
]

print(os.linesep.join(
  [l if (l == out[-1] or ((l.endswith('}') or l.startswith("\\")) and not (any([v in l for v in do_end]))))
   else l+'\\\\' for l in out]))
