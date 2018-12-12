import numpy as np

plot_type="dots"

data = """\
task:20
find:12
info:11
working:3
"""
data = [(k,int(v)) for (k,v) in [line.split(':') for line in data.splitlines()]]
label_pos = range(len(data))
labels = [t[0] for t in data]

maxy = max([t[1] for t in data])
y = []
x = []
for i, r in enumerate([range(v) for (_,v) in data]):
  l = list(r)
  x += [i]*len(l)
  y += list(r)

dot_scale = 3

labels_y = [v+1 for v in range(maxy)][3::4]
labels_pos_y = [v-1 for v in labels_y]
