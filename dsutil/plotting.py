# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt

def plot_value_labels(ax=None, format=None):

    if ax is None:
        ax = plt.gca()

    if format is None:
        format = '{:,}'

    rects = ax.patches

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
            # Invert space to place label below
            space *= -1
            # Vertically align label at top
            va = 'top'

        # Create annotation

        ax.annotate(label, (x_value, y_value), 
                      xytext=(0, 2), 
                      textcoords="offset points", 
                      ha='center', 
                      rotation=45, 
                      va=va)    


def format_yaxis_as_percentage(ax=None):

    if ax is None:
        ax = plt.gca()

    vals = ax.get_yticks()
    ax.set_yticklabels(['{:,.0%}'.format(x) for x in vals])


def add_grid(ax=None):

    if ax is None:
        ax = plt.gca()

    # enable grid lines in the axis
    ax.grid(True)

    # select both y axis and x axis
    gridlines = ax.get_xgridlines() + ax.get_ygridlines()

    # choose line width
    line_width = 0.7

    for line in gridlines:
        line.set_linestyle(':')
        line.set_linewidth(line_width)