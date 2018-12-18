#!/usr/bin/env python3

import sys
sys.path.append(".")
import config as cfg

import os
import numpy as np

out = []

def append(text):
  out.append(text)

def add(text):
  out[-1] += text

def new_page():
  append("\\newpage")

def strip_last_newline():
  out[-1] = out[-1].replace("\\\\", '')


def print_to_output():

  do_end = [
    "includegraphics"
  ]

  def cmd_end(line):
    return line.strip().endswith('}') and not any([v in line for v in do_end])

  def cmd(line):
    return line.strip().startswith("\\")

  def tikz_cmd(line):
    return cmd(line) and line.strip().endswith(';')

  endlines = []
  for line in out:
    if not any([f(line) for f in [cmd, cmd_end, tikz_cmd]]):
      line = line+"\\\\"
    endlines.append(line)

  print(os.linesep.join(endlines))

def get_tikz(caption, title="<Longer Title>", does=[], wants=[], words=[]):

  pos_title = (3.8, 4.0)

  pos_title_list_does = np.add((-1.3, -0.6),pos_title)
  pos_list_does = np.add((-0.5, -0.15),pos_title_list_does)

  append("\\begin{subfigure}[b]{0.45\\textwidth}")
  append("\\centering")
  append("\\begin{tikzpicture}")
  append("  \\draw[black, thick] (0,0) rectangle (\\textwidth,0.75\\textwidth);")
  append("  \\draw[black, thick] (0.2cm,0.75\\textwidth-0.2cm) rectangle (0.37\\textwidth-0.2cm,2cm);")
  append("  \\node [font=\Large] at ({:.2f},{:.2f}) {{{}}};".format(*pos_title, title))

  append("  \\node at ({:.2f},{:.2f}) {{{}}};".format(*pos_title_list_does, "Does:"))
  y_current = pos_list_does[1]
  for text in does:
    append("  \\node [anchor=north west, font=\\footnotesize] at ({:.2f},{:.2f}) {{{}}};".format(pos_list_does[0], y_current, "$\\bullet$ {}".format(text)))
    y_current -= 0.32

  pos_title_list_want = np.add((0.0, -0.5),(pos_title_list_does[0],y_current))
  y_current = pos_title_list_want[1] - 0.15
  append("  \\node at ({:.2f},{:.2f}) {{{}}};".format(*pos_title_list_want, "\ Wants:"))
  for text in wants:
    append("  \\node [anchor=north west, font=\\footnotesize] at ({:.2f},{:.2f}) {{{}}};".format(pos_list_does[0], y_current, "$\\bullet$ {}".format(text)))
    y_current -= 0.32

  pos_title_list_words = (0.2, 1.55)
  append("  \\node [anchor=north west] at ({:.2f},{:.2f}) {{{}}};".format(*pos_title_list_words, "Words:"))


  append("\\end{tikzpicture}")
  append("\\caption{{{}}}".format(caption))
  append("\\end{subfigure}")

def main():
  append("\\begin{figure}[H]")
  append("\\centering")
  get_tikz("The artist persona.",
           title="Adam (Artist)",
           does=['Update tasks with media.',
                 'Ask for feedback on tasks.',
                 'Update task status.'],
           wants=['Cleaner note overview.',
                  'Auto-info on task-update.',
                  'Clear communication of status changes.'])
  append("\\hfill")
  get_tikz("B")
  append("\\vskip\\baselineskip")
  get_tikz("C")
  append("\\hfill")
  get_tikz("D")
  append("\\caption{Project personas.}")
  append("\\end{figure}")
  print_to_output()


if __name__ == "__main__":
  main()
