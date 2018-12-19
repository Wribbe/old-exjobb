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

def strip_last_newline():
  out[-1] = out[-1].replace("\\\\", '')

objectives = {}
key_results = {}

def gantt():
  append(
    "\\def\\pgfcalendarweekdayletter#1{\
      \\ifcase#1M\\or T\\or W\\or T\\or F\\or S\\or S\\fi\
    }")
  append("\\newgeometry{left=3cm, bottom=1cm, footskip=0.5cm}")
  append("\\begin{landscape}")
  start = dt.today()
  delta = td(days=54)
  end = start + delta
  while True:
    if end > day_finished:
      end = day_finished
    append("\\begin{ganttchart}\
           [ \
            y unit chart = 0.6cm,x unit = 0.45cm,hgrid,vgrid,\
            milestone inline label node/.append style={left=2mm},\
            time slot format=isodate \
           ]")
    add("{{{}}}{{{}}}".format(label_iso(start),label_iso(end)))
    append("\\gantttitlecalendar{year, month=name, day, weekday=letter}")
    append("\\ganttnewline")
    dates_objs = [d for d in sorted(objectives) if start-td(days=1) <= d <= end]
    for date in dates_objs:
      for obj in objectives[date]:
        append("\\ganttmilestone{{ {} }}{{ {} }} \\\\".format(obj, label_iso(date)))
    strip_last_newline()
    append("\\ganttnewline")
    dates_krs = [d for d in sorted(key_results) if start-td(days=1) <= d <= end]
    for date in dates_krs:
      for kr, color in key_results[date]:
        ref_kr = "ref{}".format(kr)
        label = label_iso(date)
        append("\\ganttbar[\
               bar label font=\\color{{{0}}},\
               bar/.append style={{fill={0}, rounded corners=3pt}}]\
               {{ {1} }}{{ {2} }}{{ {2} }} \\\\".format(color,
                                                       # "\\hyperref[{}]{{{}}}".format(ref_kr,kr),
                                                        kr,
                                                        label))
    strip_last_newline()
    append("\\end{ganttchart}")
    append("\\newpage")
    if end == day_finished:
      break
    start = end+td(days=1)
    end += delta
  append("\\end{landscape}")
  append("\\restoregeometry")

#data = np.random.randint(0,12,size=72)
#bins = np.arange(13)-0.5

#hist, edges = np.histogram(data, bins=bins)
#y = np.arange(1,hist.max()+1)
#x = np.arange(12)
#X,Y = np.meshgrid(x,y)

mark_checked = "$\u2713$"
mark_not_checked = "$\u2610$"
mark_abandonend = "$-$"

def figure_progress(length, name, checked=[], labels_x=[]):

  fig_height = 0.67 if labels_x else 0.2
  if length == 1:
    figsize = (0.2, fig_height)
  else:
    figsize = (min(0.5*length, 5.5),fig_height)
  f = plt.figure(figsize=figsize)

  plt.scatter(range(length),[0]*length, c="black", marker=mark_not_checked)
  marker = mark_checked
  color = "green"

  if -1 in checked:
    marker = mark_abandonend
    color = "black"
    checked = range(length)
    length = -1

  for x in checked:
    if marker == mark_abandonend:
      y = -0.05
      for dx in range(-2,3):
        plt.scatter(x+dx,y, marker=marker, c=color)
    else:
      plt.scatter(x,0, marker=marker, c=color)
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
  plt.close()
  return (path_fig, length, len(checked))

day_start = dt.strptime("2018-12-13", "%Y-%m-%d")
fmt_month = "%d/%m"
mondays = [day_start + td(days=x) for x in
           range(10*7+1) if (day_start+td(days=x)).weekday() == 0]
labels_mondays = [dt.strftime(d, fmt_month) for d in mondays]


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
  if date:
    os = objectives.get(date)
    if not os:
      os = objectives[date] = []
    os.append("O{}".format(count_O))

def keyresult(text, data_img, date=None):
  global count_KR
  image, tot_checkable , num_checked = data_img
  if tot_checkable == -1: # Abandoned.
    prog = -1
  else:
    prog = num_checked / tot_checkable

  if prog == -1:
    color = "gray"
  elif prog < 0.3:
    color = "red"
  elif prog < 0.7:
    color = "yellow"
  else:
    color = "green"

  fmt_kr = "\\hypertarget{{{0}}}{{\\mybox[fill={1}!20]{{\\textbf{{{0}:}}}} \\\\ {2}}}"
  count_KR += 1
  if date:
    text = text.format(label_weekdate(date))
  kr_tag = "KR{}.{}".format(count_O, count_KR)
  if prog == -1:
    kr_tag = "\\sout{{{}}}".format(kr_tag)
    text = "\\sout{{{}}}".format(text)
  append(fmt_kr.format(kr_tag, color, text))
#  append("\\vspace{0.3cm}")
  append("\\begin{center}")
  append("\\includegraphics")
  add("{{{}}}".format(image))
  append("\\end{center}")
  if date:
    krs = key_results.get(date)
    if not krs:
      krs = key_results[date] = []
    krs.append((kr_tag, color))

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
keyresult("Email expanded draft each Monday for 10 weeks.",
          figure_progress(10, "draft_mondays",
                          labels_x=labels_mondays,
                          checked=[0,]))

keyresult(
  fmt_in_person.format("LTH", "{}"),
  figure_progress(3,"presentation_LTH",checked=[]),
  day_last_draft_presentation)
keyresult(
  fmt_in_person.format("MASSIVE", "{}"),
  figure_progress(3,"presentation_MASSIVE"),
  day_last_draft_presentation)
keyresult("Finalize and email / handout this OKR document no later than {}.",
  figure_progress(1,"finalize_OKRs",checked=[0]),
  days_from_start(1))

objective("Do opposition on interesting master thesis.")
keyresult("Find 8 promising thesis projects no later than {}.",
  figure_progress(8,"found_opposition_thesis", checked=[0]),
  days_from_start(7))
keyresult("Contact at least three students of the eight no later than {}.",
  figure_progress(3,"selected_opposition_thesis"),
  days_from_start(7+12+7))
keyresult("Final opposing thesis confirmed no later than {}.",
  figure_progress(1,"final_opposition_thesis"),
  days_from_start(7+12+7*3))


objective(
  "Ensure a robust grounding in scientific literature.")
keyresult(
  "Find and save at least 15 promising articles to reference, no later than {}.",
  figure_progress(15,"references_articles"),
  days_from_start(7+12+3))
keyresult(
  "Find at least 3 promising books to references, no later than {}.",
  figure_progress(3,"references_books", checked=[0,1,2]),
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
  figure_progress(1,"create_personas", checked=[0]),
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

day_test_interface_theory = day_start+td(days=7*2)

objective(
  "Figure out how to test interface-theory no later than {}.",
  day_test_interface_theory)
keyresult(
  "Execute runnable example on current web-backend no later than {}.",
  figure_progress(1,"interface_theory_backend", checked=[0]),
  day_start+td(days=4))

keyresult(
  "Find alternative if current web-backend does not work no later than {}.",
  figure_progress(1,"interface_theory_backend_alternative", checked=[-1]),
  day_start+td(days=6))
keyresult(
  "Showcase to supervisor and company contacts no later than {}.",
  figure_progress(3,"interface_theory_backend_showcase"),
  day_test_interface_theory-td(days=6))

append("\\end{adjustwidth}")
append("\\restoregeometry")

gantt()

do_end = [
  "includegraphics"
]

print(os.linesep.join(
  [l if (l == out[-1] or ((l.endswith('}') or l.startswith("\\")) and not (any([v in l for v in do_end]))))
   else l+'\\\\' for l in out]))
