code = """\
  \\begin{ganttchart}{1}{12}
  \\gantttitle{2011}{12} \\\\
  \\gantttitlelist{1,...,12}{1} \\\\
  \\ganttgroup{Group 1}{1}{7} \\\\
  \\ganttbar{Task 1}{1}{2} \\\\
  \\ganttlinkedbar{Task 2}{3}{7} \\ganttnewline
  \\ganttmilestone{Milestone}{7} \\ganttnewline
  \\ganttbar{Final Task}{8}{12}
  \\ganttlink{elem2}{elem3}
  \\ganttlink{elem3}{elem4}
  \\end{ganttchart}
"""

def cmd(l, opts=[], endl=True):
    command, params = l[0], l[1:]
    string = "\\{}".format(command)
    if opts:
        string += "[{}]".format(','.join(*opts))
    for par in params:
        string += "{{{}}}".format(par)
    if endl:
        string += "\\\\"
    return string

def gantt(start, end, title="default"):
    return {
        "start": start,
        "end": end,
        "title": title,
        "tasks": [],
        "groups": [],
    }

def print_gantt(g):
    start, end = g["start"], g["end"]
    size = end - start + 1
    lines = [cmd(["begin","ganttchart","1",size], endl=False)]
    lines.append(cmd(["gantttitle", g["title"], size]))
    lines.append(cmd(["gantttitlelist", "{},...,{}".format(start, end), "1"]))
    for variant, opts, t_start, t_stop, t_name in g["tasks"]:
        command = "ganttbar"
        if variant is 'G':
            command = "ganttgroup"
        else:
            filter_opts = []
            for optlist in opts:
                if not any(["group" in opt.split() for opt in optlist]):
                    filter_opts.append(optlist)
            opts = filter_opts
        lines.append(cmd([command, t_name, t_start+1, t_stop+1], opts=opts))
    lines.append(cmd(["end" ,"ganttchart"], endl=False, opts=opts))
    print('\n'.join(lines))

#print(
#"""
#  \\begin{ganttchart}{1}{42}
#  \\gantttitlelist{1,...,42}{1} \\\\
#  \\end{ganttchart}
#"""
#)

#print(code)

weeks_total = 20
days_per_week = 5
days_total = weeks_total*days_per_week
split = 39

charts = []

day_current = 0
while day_current < days_total:
    day_start = day_current
    day_end = day_start + split
    if day_end > days_total:
        day_end = days_total
    charts.append(gantt(day_start, day_end))
    day_current += split + 1

tasks = [
    ('G', 0, 10, "GROUPTEST"),
    ('T', 4, 41, "TEST"),
    ('T', 2, 82, "TEST2"),
    ('G', 5, 83, "GROUPTEST"),
    ('T', 2, 82, "TEST2"),
]

group_no_left = ["group left peak height = 0", "group left shift = 0"]
group_no_right = ["group right peak height = 0", "group right shift = 0"]
group_none = group_no_left + group_no_right

for task in tasks:
    variant, t_start, t_end, t_name = task
    for chart in charts:
        c_start, c_end = chart["start"], chart["end"]
        if t_start >= c_start:
            if t_end <= c_end:
                chart["tasks"].append((task[0], [], *task[1:]))
            else:
                chart["tasks"].append((variant, [group_no_right], t_start, c_end, t_name))
        elif t_start < c_start and t_end >= c_start and  t_end <= c_end:
            chart["tasks"].append((variant, [group_no_left], 0, t_end-c_start, t_name))
        elif t_start <= c_start and t_end >= c_end:
            chart["tasks"].append((variant, [group_none], 0, c_end-c_start, t_name))

for chart in charts:
    print_gantt(chart)
