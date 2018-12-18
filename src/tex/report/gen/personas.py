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


  # Pictures from: https://www.userpersonaimages.com/
  # Using shapes: https://www.cxpartners.co.uk/our-thinking/dont-use-photos-in-your-personas/

  pos_title = (4.1, 4.3)

  pos_title_list_does = np.add((-1.3, -0.45),pos_title)
  pos_list_does = np.add((-0.5, -0.15),pos_title_list_does)

  append("\\begin{subfigure}[b]{0.495\\textwidth}")
  append("\\centering")
  append("\\begin{tikzpicture}")
  append("  \\draw[black, thick] (0,0) rectangle (\\textwidth,0.75\\textwidth);")
  append("  \\draw[black, thick] (0.1cm,0.1cm) rectangle (\\textwidth-0.1cm,0.75\\textwidth-0.1cm);")
  append("  \\node at (1.2,3.3) {{\includegraphics[width=1.7cm]{{images/{}.pdf}}}};".format(title.split(' ')[0].lower()))
  append("  \\draw[black, thick] (0.2cm,0.75\\textwidth-0.2cm) rectangle (0.37\\textwidth-0.2cm,2cm);")
  append("  \\node [font=\Large] at ({:.2f},{:.2f}) {{{}}};".format(*pos_title, title))

  append("  \\node at ({:.2f},{:.2f}) {{{}}};".format(*pos_title_list_does, "Does:"))
  y_current = pos_list_does[1]

  for text in does:
    rest = []
    if type(text) is list:
      text, rest = text[0], text[1:]
    append("  \\node [anchor=north west, font=\\footnotesize] at ({:.2f},{:.2f}) {{{}}};".format(pos_list_does[0], y_current, "$\\bullet$ {}".format(text)))
    y_current -= 0.32
    for sentence in rest:
      append("  \\node [anchor=north west, font=\\footnotesize] at ({:.2f},{:.2f}) {{{}}};".format(pos_list_does[0], y_current, "\hspace{{0.18cm}} {}".format(sentence)))
      y_current -= 0.32

  pos_title_list_want = np.add((0.0, -0.4),(pos_title_list_does[0],y_current))
  y_current = pos_title_list_want[1] - 0.15
  append("  \\node at ({:.2f},{:.2f}) {{{}}};".format(*pos_title_list_want, "\ Wants:"))
  for text in wants:
    rest = []
    if type(text) is list:
      text, rest = text[0], text[1:]
    append("  \\node [anchor=north west, font=\\footnotesize] at ({:.2f},{:.2f}) {{{}}};".format(pos_list_does[0], y_current, "$\\bullet$ {}".format(text)))
    y_current -= 0.32
    for sentence in rest:
      append("  \\node [anchor=north west, font=\\footnotesize] at ({:.2f},{:.2f}) {{{}}};".format(pos_list_does[0], y_current, "\hspace{{0.18cm}} {}".format(sentence)))
      y_current -= 0.32

  pos_title_list_words = (0.1, 2.00)
  append("  \\node [anchor=north west] at ({:.2f},{:.2f}) {{{}}};".format(*pos_title_list_words, "Words {\\small(>1)}:"))
  y_current = pos_title_list_words[1] - 0.38
  fmt_node = "\\node \
    [anchor=north west, font=\\footnotesize] \
    at ({:.2f},{:.2f}) {{\\texttt{{{}}}}};"
  if words:
    max_len = max([len(w) for w,_ in words])
  for word, num in words:
    append(fmt_node.format(pos_title_list_words[0]+0.03, y_current, "{}{}{}".format(word,'\\ '*(max_len-len(word)+1),num)))
    y_current -= 0.32



  append("\\end{tikzpicture}")
  append("\\caption{{{}}}".format(caption))
  append("\\end{subfigure}")

def main():
  append("\\begin{figure}[H]")
  append("\\centering")
  get_tikz("The artist persona.",
           title="Arden",
           does=['Update tasks with media.',
                 'Ask for feedback on tasks.',
                 'Update task statuses.'],
           wants=['Cleaner notes overview.',
                  ['Auto-completion when', 'updating media on a task.'],
                  ['Automatic communication', 'of status changes.']],
           words=[("Lacking",3),
                  ("Complex", 2),
                  ("Functional", 2),
                  ("Okay", 2),
                  ])
  get_tikz("The animator persona.",
           title="Andi",
           does=[['Communicate with others', 'assigned to the same task.'],
                 'Gather task information.',
                 'Find assigned tasks.'],
           wants=['Cascading task statuses.',
                  'Less email update-spam.',
                  ['Customizable data', 'organization.']],
           words=[
                    ("Functional", 2),
                    ("Okay",2),
                  ])
  get_tikz("The manager persona.",
           title="Maslon",
           does=['Feedback to Arden \& Andi.',
                 ['Manage workload and', 'schedules.'],
                 'Creating tasks.'],
           wants=[['Possibility to combine', 'views into multi-views.'],
                  'User KANBAN boards.',
                  ['More streamlined thought-', 'to-task flow.']],
           words=[("Lacking",2),
                  ("Functional", 2),
                  ])
  get_tikz("The technician persona.",
           title="Tegan",
           does=['Create and manage tasks.',
                 ['System development and', 'maintenance.'],
                 'Formulate goals into tasks.'],
           wants=[['Better production status', 'graphs.'],
                  'Batch-updating on tasks.',
                  ['Simplified input flow for', 'task creation.']],
           words=[("Understa..",2),
                  ("Functional", 2),
                  ("Delightful", 2),
                  ])
#  get_tikz("B")
#  append("\\vskip\\baselineskip")
#  get_tikz("C")
#  get_tikz("D")
  append("\\caption{Project personas.}")
  append("\\end{figure}")
  print_to_output()


if __name__ == "__main__":
  main()
