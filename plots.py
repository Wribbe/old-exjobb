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
        "ticks_x": "",
        "ticks_y": "",
        "title": "",
        "size": DEFAULT_SIZE,
    },
    'pie': {
        "explode": lambda module: [0]*len(module.labels),
        "title": "",
        "size": DEFAULT_SIZE,
        "colors": None,
    },
    'bar': {
        "label_x": "",
        "label_y": "",
        "title": "",
        "formatter": None,
        "size": DEFAULT_SIZE,
    },
    'dots': {
      "label_x": "",
      "label_y": "",
      "title": "",
      "size": DEFAULT_SIZE,
      "rotation_label": None,
      "dot_scale":3.0,
      "labels_y": [],
      "rotate_figure": False,
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
        f = plt.figure(figsize=(figure.size))
        patches, text = plt.pie(figure.values, explode=figure.explode,
                               startangle=90, colors=figure.colors)
        plt.legend(patches, labels=figure.labels, loc="best",
                  prop={'size': 5})
        plt.tight_layout()
#        ax.set_axis_off()
    elif figure.plot_type == "bar":
        f, ax = plt.subplots(figsize=figure.size)
        plt.bar(figure.x, figure.x_data)
        plt.xticks(figure.x, figure.x_ticks)
        if figure.formatter:
            formatter = FuncFormatter(figure.formatter)
            ax.yaxis.set_major_formatter(formatter)
    elif figure.plot_type == "dots":
      f, ax = plt.subplots(figsize=figure.size)
      if figure.rotate_figure:
        ax.scatter(figure.y, figure.x, s=figure.dot_scale)
        plt.yticks(figure.label_pos, figure.labels, rotation=figure.rotation_label)
        plt.xticks(figure.labels_pos_y, figure.labels_y)
      else:
        ax.scatter(figure.x, figure.y, s=figure.dot_scale)
        plt.xticks(figure.label_pos, figure.labels, rotation=figure.rotation_label)
        plt.yticks(figure.labels_pos_y, figure.labels_y)

    else: # type == "line".
        f = plt.figure(figsize=figure.size)
        plt.plot(figure.x, figure.y)
        if figure.label_x:
            fig.xlabel(figure.label_x, **hfont)
        if figure.label_y:
            fig.ylabel(figure.label_y, **hfont)
        if figure.ticks_x:
          plt.xticks(*figure.ticks_x[:2], **figure.ticks_x[2])
        if figure.ticks_y:
          plt.yticks(*figure.ticks_y[:2], **figure.ticks_y[2])

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
    if figure.plot_type == "pie":
      f.savefig(path_output)
    else:
      f.savefig(path_output, bbox_inches='tight', pad_inches=-0.0)

if __name__ == "__main__":
   main(sys.argv[1:])
