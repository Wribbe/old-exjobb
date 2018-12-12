import sys
sys.path.append(".")

import sqlite3
import config as cfg
import datetime

from collections import Counter

conn = sqlite3.connect(cfg.PATH_DATABASE)

cs = conn.execute("""
  SELECT time FROM submission JOIN survey ON submission.id_survey = survey.id
  WHERE survey.filename LIKE "%001_initial%"
""").fetchall()

cs = [c[0] for c in cs]
fmt_date = "%Y-%m-%d"
fmt_month = "%d/%m"
dates = [datetime.datetime.strptime(c, "{} %H:%M:%S".format(fmt_date)) for c in cs]

first = datetime.datetime.strptime("2018-11-12", fmt_date)
last =  dates[-1]
count_dates = Counter()

def timerange(start, end):
  return [start + datetime.timedelta(days=x) for x in
          range(0, (end-start).days+1)]

for d in dates:
  str_date = datetime.datetime.strftime(d, fmt_month)
  count_dates[str_date] += 1

labels_dates = [datetime.datetime.strftime(d, fmt_month) for d in
                timerange(first, last)]

plot_type="line"
x = range(len(labels_dates))
y = [count_dates.get(l,0) for l in labels_dates]
ticks_x = (x, labels_dates, {'rotation': 90})
ticks_y_range = range(max(count_dates.values())+1)
ticks_y = (ticks_y_range, ticks_y_range, {})
