# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt


def plot_value_labels(ax=None, format=None):
    if ax is None:
        ax = plt.gca()

    if format is None:
        format = '{:,}'

    rects = ax.patches

    if len(rects) == 0:
        raise Exception('Right now this method only works for bar charts')

    # For each bar: Place a label
    for rect in rects:

        # Get X and Y placement of label from rect.
        y_value = rect.get_height()
        x_value = rect.get_x() + rect.get_width() / 2

        label = format.format(y_value)

        # Vertical alignment for positive values
        va = 'bottom'

        # If value of bar is negative: Place label below bar
        if y_value < 0:
            # Vertically align label at top
            va = 'top'

        # Create annotation
        ax.annotate(label, (x_value, y_value),
                    xytext=(0, 2),
                    textcoords="offset points",
                    ha='center',
                    rotation=45,
                    va=va)


def format_yaxis_percentage(ax=None, fmt=None):
    if ax is None:
        ax = plt.gca()

    if fmt is None:
        fmt = '{:,.0%}'

    current_values = ax.get_yticks()
    ax.set_yticklabels([fmt.format(x) for x in current_values])


def format_yaxis_thousands(ax=None, fmt=None):
    if ax is None:
        ax = plt.gca()

    if fmt is None:
        fmt = '{:,}'

    current_values = ax.get_yticks()
    ax.set_yticklabels([fmt.format(x) for x in current_values])


def add_grid(ax=None, line_width=None):
    if ax is None:
        ax = plt.gca()

    # enable grid lines in the axis
    ax.grid(True)

    # select both y axis and x axis
    gridlines = ax.get_xgridlines() + ax.get_ygridlines()

    if line_width is None:
        # choose line width
        line_width = 0.7

    for line in gridlines:
        line.set_linestyle(':')
        line.set_linewidth(line_width)
