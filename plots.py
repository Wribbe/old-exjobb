#!/usr/bin/env python3

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import importlib.util

NUM_FIG = 0
DEFAULT_SIZE = (3.0, 1.5)

hfont = {'fontname': 'Helvetica'}

defaults = {
    'line': {
        "label_x": "",
        "label_y": "",
        "title": "",
        "size": DEFAULT_SIZE,
    },
    'pie': {
        "explode": lambda module: [0]*len(module.labels),
        "title": "",
        "size": DEFAULT_SIZE,
    },
    'bar': {
        "label_x": "",
        "label_y": "",
        "title": "",
        "formatter": None,
        "size": DEFAULT_SIZE,
    },
}

def check_default_attributes(module):
    for attrib, default in defaults[module.plot_type].items():
        if not hasattr(module, attrib):
            try:
                setattr(module, attrib, default(module))
            except TypeError: # Not a function.
                setattr(module, attrib, default)


def create_plot(figure):

    if figure.title:
        plt.title(figure.title, **hfont)

    if figure.plot_type == "pie":
        f, ax = plt.subplots(figsize=figure.size)
        ax.pie(figure.values , explode=figure.explode, labels=figure.labels,
                autopct='%1.1f%%', shadow=True, startangle=90)
        ax.set_axis_off()
    elif figure.plot_type == "bar":
        f, ax = plt.subplots(figsize=figure.size)
        plt.bar(figure.x, figure.x_data)
        plt.xticks(figure.x, figure.x_ticks)
        if figure.formatter:
            formatter = FuncFormatter(figure.formatter)
            ax.yaxis.set_major_formatter(formatter)

    else: # type == "line".
        f = plt.figure(figsize=figure.size)
        plt.plot(figure.x, figure.y)
        if figure.label_x:
            fig.xlabel(figure.label_x, **hfont)
        if figure.label_y:
            fig.ylabel(figure.label_y, **hfont)

    return f

def main(arguments):

    if len(arguments) < 2:
        print("Need at least 2 arguments.")
        sys.exit()

    path_module, path_output = arguments

    spec = importlib.util.spec_from_file_location("figure", path_module)
    figure = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(figure)

    dir_figs = os.path.dirname(path_output)
    if not dir_figs:
        dir_figs = "."
    if not os.path.isdir(dir_figs):
        os.makedirs(dir_figs)

    check_default_attributes(figure)

    f = create_plot(figure)
    f.savefig(path_output, bbox_inches='tight', pad_inches=-0.0)

if __name__ == "__main__":
   main(sys.argv[1:])
