plot_type="bar"

data = [
    ('Bill', 1.5e5),
    ('Fred', 2.5e6),
    ('Mary', 5.5e6),
    ('Sue', 2.0e7),
]

def millions(x, pos):
    return "${:1.1f}M".format(x * 1e-6)

x = range(len(data))
x_ticks = []
x_data = []
for tick, data in data:
    x_ticks.append(tick)
    x_data.append(data)
formatter = millions
