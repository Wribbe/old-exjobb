#!/usr/bin/env python3

import sys
import re
import os

def main(args):
  tex_file=args.pop(0)
  args_dict = {k.strip():v.strip() for (k,v) in
               [arg.split('=') for arg in args if '=' in arg]}
  text = open(tex_file).read()
  for key, value in args_dict.items():
    text = re.sub(r'\${}'.format(key), value, text)
  if "COMMENTS" in args:
    text = os.linesep.join(["\\def\\visibleComments{1}",text])
  elif "NO_APPENDIX" in args:
    out = []
    in_appendice = False
    for line in text.splitlines():
      if "section{Appendices}" in line:
        in_appendice = True
      elif in_appendice and "section{" in line:
        in_appendice = False
      if in_appendice:
        continue
      out.append(line)
    text = os.linesep.join(out)

  print(text)

if __name__ == "__main__":
  main(sys.argv[1:])
