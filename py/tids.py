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
    if params[0] == 'ganttchart':
        string += "{{{}}}".format(params[0])
        params = params[1:]
    if command == 'ganttmilestone': # Drop last parameter (end).
        params = params[:2]
    if opts:
        if type(opts[0]) is not list:
            opts = [opts]
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
    g_opts = ["y unit chart = 0.6cm", "x unit = 0.45cm", "hgrid", "vgrid"]
    lines = [cmd(["begin","ganttchart","1",size], endl=False, opts=g_opts)]
#    lines.append(cmd(["gantttitle", g["title"], size]))
    lines.append(cmd(["gantttitlelist", "{},...,{}".format(start, end), "1"]))
    for variant, t_start, t_stop, t_name, opts in g["tasks"]:
        command = "ganttbar"
        if variant is 'G':
            command = "ganttgroup"
        elif variant is 'M':
            command = "ganttmilestone"
        else:
            filter_opts = []
            for optlist in opts:
                if not any(["group" in opt.split() for opt in optlist]):
                    filter_opts.append(optlist)
            opts = filter_opts
        lines.append(cmd([command, t_name, t_start, t_stop], opts=opts))
    lines[-1] = lines[-1][:-2]
    lines.append(cmd(["end" ,"ganttchart"], endl=False))
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
days_total = weeks_total*days_per_week+1
split = 38

charts = []

day_current = 1
while day_current < days_total:
    day_start = day_current
    day_end = day_start + split
    if day_end > days_total:
        day_end = days_total
    charts.append(gantt(day_start, day_end))
    day_current += split + 1

pilot = [
         ("Förintervjuer", 4),
         ("mod", -2),
         ("Utkast formulär", 3),
         ("mod", -2),
         ("Utvärdering formulär", 3),
         ("mod", -1),
         ("Implementering pilot-UI", 7),
         ("mod", -3),
         ("Utvärdering pilot-UI", 3),
        ]

def spread(l, start=1):
    current = start
    tuples = []
    for name, length in l:
        if name == "mod":
            current += length
            continue
        tuples.append(("T", current, current+length-1, name))
        current += length
    return current-1, tuples

pilot_start = 3
pilot_end, pilot_tasks = spread(pilot, start=pilot_start)

litstudy = [
    ("Leta relevant litteratur", 12),
    ("mod", -4),
    ("Utvärdera litteratur", 7),
]

litstudy_start = pilot_end + 1
litstudy_end, litstudy_tasks = spread(litstudy, start=litstudy_start)

pilot2_num = 8
pilot2 = [
    ("Implementering studie-UI", pilot2_num),
    ("mod", -pilot2_num),
    ("Färdigställ studie-formulär", pilot2_num),
    ("mod", -4),
    ("Välj kandidater för studie", 4),
]

pilot2_start = litstudy_end + 1
pilot2_end, pilot2_tasks = spread(pilot2, start=pilot2_start)


studie1 = [
    ("Genomförande", 5),
    ("Utvärdering", 2),
]

studie1_start = pilot2_end + 1
studie1_end, studie1_tasks = spread(studie1, start=studie1_start)

iter1 = [
    ("Modifiering UI", 4),
    ("mod", -4),
    ("Modifiering formulär", 4),
]

iter1_start = studie1_end+1+2
iter1_end, iter1_tasks = spread(iter1, start=iter1_start)


studie2 = [
    ("Genomförande", 5),
    ("Utvärdering", 2),
]

studie2_start = iter1_end + 1
studie2_end, studie2_tasks = spread(studie2, start=studie2_start)

iter2_start = studie2_end+2+1
iter2_end, iter2_tasks = spread(iter1, start=iter2_start)

studie3_start = iter2_end + 1
studie3_end, studie3_tasks = spread(studie2, start=studie3_start)

sammanställning = [
    ("Bearbeta data", 15),
    ("mod", -5),
    ("Slutintervjuer", 5),
]

sammanställning_start = studie3_end+1
sammanställning_end, sammanställning_tasks = spread(sammanställning,
                                                      start=sammanställning_start)


tasks = [
    ('T', 1, 2, "Uppstart"),
    ('G', pilot_start, pilot_end, "Pilot"),
    *pilot_tasks,
    ('G', litstudy_start, litstudy_end, "Literaturstudie"),
    *litstudy_tasks,
    ('G', pilot2_start, pilot2_end, "Förbered studie"),
    *pilot2_tasks,
    ('M', pilot2_end, 0, "Frys UI och formulär"),
    ('G', studie1_start, studie1_end, "Studie \#1"),
    *studie1_tasks,
    ('T', studie1_end+1, studie1_end+2, "ev. ytterligare litteratur"),
    ('G', iter1_start, iter1_end, "Återkoppling \#1"),
    *iter1_tasks,
    ('M', iter1_end, 0, "Frys UI och formulär\#2"),
    ('G', studie2_start, studie2_end, "Studie \#2"),
    *studie2_tasks,
    ('T', studie2_end+1, studie2_end+2, "ev. ytterligare litteratur"),
    ('G', iter2_start, iter2_end, "Återkoppling \#2"),
    *iter2_tasks,
    ('M', iter2_end, 0, "Frys UI och formulär\#3"),
    ('G', studie3_start, studie3_end, "Studie \#3"),
    *studie3_tasks,
    ('G', sammanställning_start, sammanställning_end, "Sammanställning"),
    *sammanställning_tasks,
    ('T', 77, 92, "Opponering"),
    ('T', 38, 90, "Skriva rapport"),
    ('T', days_total-6, days_total, "Presentationsförberedelser"),
]

group_no_left = ["group left peak height = 0", "group left shift = 0"]
group_no_right = ["group right peak height = 0", "group right shift = 0"]
group_none = group_no_left + group_no_right

def normalize_task(task, c_start):
    variant, start, stop, name = task
    start, stop = [s-c_start+1 for s in [start, stop]]
    return (variant, start, stop, name)

for task in tasks:
    variant, t_start, t_end, t_name = task
    for chart in charts:
        c_start, c_end = chart["start"], chart["end"]
        if t_start >= c_start:
            if t_end <= c_end:
                if variant == 'M' and not c_end >= t_start:
                    continue
                chart["tasks"].append((*normalize_task(task, c_start), []))
            elif t_start < c_end:
                chart["tasks"].append((variant, t_start-c_start+1, c_end-c_start+1, t_name, [group_no_right]))
        elif t_start < c_start and t_end >= c_start and  t_end <= c_end:
            chart["tasks"].append((variant, 1, t_end-c_start+1, t_name, [group_no_left]))
        elif t_start <= c_start and t_end >= c_end:
            chart["tasks"].append((variant, 1, c_end-c_start+1, t_name, [group_none]))

for chart in charts:
    print_gantt(chart)
