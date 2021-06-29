# -*- coding: utf-8 -*-

import itertools

import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import confusion_matrix


def add_value_labels(ax=None, fmt=None, rotation=None, **kwargs):
    # backwards compatibility
    if kwargs.get('format', None) is not None:
        fmt = kwargs['format']

    if ax is None:
        ax = plt.gca()

    if fmt is None:
        fmt = '{:,.0f}'

    if rotation is None:
        rotation = 0

    absolute_distance_in_points = 5
    integer_fmt = "{:,}"

    # ax.patches return rectangles (e.g. generated by bar plots)
    # ax.collections return path collections (such as those generated by scatter plots)
    # ax.lines return Line2D objects (such as those generated by line plots)

    patches = ax.patches
    lines = ax.lines
    collections = ax.collections

    if len(patches) != 0:
        # it's a bar plot

        # For each bar: Place a label
        for rect in patches:
            # Get X and Y placement of label from rect.
            y_value = rect.get_height()
            x_value = rect.get_x() + rect.get_width() / 2

            # maybe the value is an integer not a float
            label = _build_label_from_yvalue(y_value, integer_fmt, fmt)

            va, ytext = _build_label_params_from_yvalue(y_value, absolute_distance_in_points)

            # Create annotation
            ax.annotate(label, (x_value, y_value),
                        xytext=(0, ytext),
                        textcoords="offset points",
                        ha='center',
                        rotation=rotation,
                        va=va)
    elif len(lines) == 1:
        # it's a line plot

        line_plot = lines[0]

        xs, ys = line_plot.get_data()

        for (x_value, y_value) in zip(xs, ys):

            # maybe the value is an integer not a float
            if isinstance(y_value, (int, np.integer)):
                label = integer_fmt.format(y_value)
            else:
                label = fmt.format(y_value)

            va, ytext = _build_label_params_from_yvalue(y_value, absolute_distance_in_points)

            # Create annotation
            ax.annotate(label, (x_value, y_value),
                        xytext=(0, ytext),
                        textcoords="offset points",
                        ha='center',
                        rotation=rotation,
                        va=va)

    else:
        raise ValueError('Right now this method only works for bar charts and for line charts.')


def calibration_accuracy_plot(y_true,
                              y_pred,
                              ax=None,
                              plot_values_for_buckets=None,
                              plot_values_for_accuracies=None):
    if y_true.shape != y_pred.shape:
        raise ValueError(
            'Expected y_true and y_pred to have the same shapes, got {} and {}'.format(y_true.shape, y_pred.shape))

    if set(y_true) != set([0, 1.]) and set(y_true) != set([0]) and set(y_true) != set([1.]):
        raise ValueError(
            'Expected y_true to contain only 1.0 and 0.0, got {} instead'.format(set(y_true)))

    if ax is None:
        plt.clf()
        ax = plt.gca()

    if plot_values_for_buckets is None:
        plot_values_for_buckets = True

    if plot_values_for_accuracies is None:
        plot_values_for_accuracies = True

    y_label_left = 'number of predictions in bucket'
    y_label_right = 'average accuracy per bucket'
    x_label = 'score buckets'
    main_color = 'darkcyan'
    secondary_color = 'darkorange'
    bar_width = 0.7

    num_bins = 10
    num_ticks = 11

    min_x = 0.0
    max_x = 1.0

    epsilon = 0.001

    score_bins = np.arange(0, 1, (1.0 / num_bins))
    # need to add epsilon otherwise arange wont include the last number
    score_bins_with_endpoint = np.arange(0, 1 + epsilon, (1.0 / num_bins))

    # hist contains the number of elements per bin
    hist, bin_edges = np.histogram(y_pred, bins=score_bins)

    # will use these are the histogram bins
    bin_edges_with_right_edge = np.append(bin_edges, 1.0)

    bin_indexes = np.digitize(y_pred, bin_edges)
    element_bins = bin_edges[bin_indexes - 1]

    # PLOT BUCKET HISTOGRAM
    ax.hist(
        y_pred,
        bins=score_bins_with_endpoint,
        rwidth=bar_width,
        color=main_color
    )

    ax.set_ylabel(y_label_left, color=main_color)

    # make a 2d list of the form [bucket, y_actual, y_predicted]
    # [
    #  [ 0.90 , 1 , 0.92 ],
    #  [ 0.80 , 0 , 0.81 ],
    #  [ 0.55 , 0 , 0.55 ]
    # ]
    merged = np.hstack([
        element_bins.reshape(-1, 1),
        y_true.reshape(-1, 1),
        y_pred.reshape(-1, 1)
    ])

    merged_sorted = merged[merged[:, 0].argsort()]

    # https://stackoverflow.com/a/43094244
    grouped = np.split(merged_sorted[:, 1], np.cumsum(np.unique(merged_sorted[:, 0], return_counts=True)[1])[:-1])

    averages_by_bucket = np.hstack([
        np.unique(merged_sorted[:, 0]).reshape(-1, 1),
        np.array([np.mean(g) for g in grouped]).reshape(-1, 1)
    ])

    # PLOT ACCURACY LINE PLOT
    ax2 = ax.twinx()
    slack_x = 0.05  # must be half the width of one bucket
    ax2.plot(averages_by_bucket[:, 0] + slack_x, averages_by_bucket[:, 1],
             linewidth=2.0,
             linestyle='solid',
             marker='o',
             color=secondary_color,
             markeredgecolor=secondary_color,
             markerfacecolor=secondary_color)

    # CONFIGURE RIGHT AXIS
    ax2.set_ylim(0, 1.0)
    ax2.set_yticks(np.arange(0, 1.0, 0.1))
    ax2.yaxis.set_major_locator(plt.LinearLocator(numticks=num_ticks))
    ax2.set_yticklabels(['{:.0f}%'.format(x * 100 // 1) for x in ax2.get_yticks()], color=secondary_color)

    ax2.set_ylabel(y_label_right, color=secondary_color)

    # CONFIGURE LEFT AXIS

    max_value_left_axis = hist.max()
    # use slack to make space for the labels above the bars
    slack_y = 1.15
    ax.set_ylim(0, int(max_value_left_axis * slack_y))
    ax.set_yticks(np.arange(0, max_value_left_axis))
    ax.yaxis.set_major_locator(plt.LinearLocator(numticks=num_ticks))
    ax.set_yticklabels(['{:.0f}'.format(x) for x in ax.get_yticks()], color=main_color)

    if plot_values_for_buckets:
        add_value_labels(ax=ax, fmt='{:,.0f}', rotation=0)

    if plot_values_for_accuracies:
        # not using plotting.plot_value_labels because I need to plot the percentage values
        # not the actual values (0.1,0.2, etc) and because I need to see it the value is too
        # high, in which case i'll need to write it below the point, not above.
        line_plot = ax2.lines[0]
        xs, ys = line_plot.get_data()

        for (x_value, y_value) in zip(xs, ys):

            offset = 0.02
            # If value of bar is too near the top border: Place label below bar
            if y_value > 0.9:
                # Vertically align label at top
                offset = -0.1

            label = '{:.0f}%'.format(y_value * 100)
            # # Create annotation
            ax2.annotate(label, (x_value, y_value + offset),
                         xytext=(0, 2),
                         textcoords="offset points",
                         ha='center',
                         rotation=0,
                         va='bottom')

    add_grid(ax2)

    # FINALLY, CONFIGURE THE COMMON X AXIS
    ax.set_xlabel(x_label)
    ax.set_xticks(score_bins_with_endpoint)

    plt.show()


def plot_confusion_matrix(y_true,
                          y_pred,
                          class_names,
                          ax=None,
                          cmap=None,
                          colorbar=None,
                          include_labels=None,
                          normalize=None,
                          show=None):
    if y_true.shape != y_pred.shape:
        raise ValueError(
            'Expected y_true and y_pred to have the same shapes, got {} and {}'.format(y_true.shape, y_pred.shape))

    if ax is None:
        plt.clf()
        ax = plt.gca()

    if cmap is None:
        cmap = plt.cm.Blues

    if colorbar is None:
        colorbar = False

    if include_labels is None:
        include_labels = True

    if normalize is None:
        normalize = False

    if show is None:
        show = True

    matrix = confusion_matrix(y_true, y_pred)

    if normalize:
        fmt = '.2f'
        matrix = matrix.astype('float') / matrix.sum(axis=1)[:, np.newaxis]
    else:
        fmt = 'd'

    ax.xaxis.tick_top()
    ax.xaxis.set_label_position('top')

    img = ax.imshow(matrix, interpolation='nearest', cmap=cmap)

    if colorbar:
        ax.get_figure().colorbar(img)

    if include_labels:
        thresh = matrix.max() / 2.
        for i, j in itertools.product(range(matrix.shape[0]), range(matrix.shape[1])):
            ax.text(j, i, format(matrix[i, j], fmt),
                    horizontalalignment="center",
                    color="white" if matrix[i, j] > thresh else "black")

    tick_marks = np.arange(len(class_names))
    ax.set_xticks(tick_marks)
    ax.set_xticklabels(class_names, rotation=45)

    ax.set_yticks(tick_marks)
    ax.set_yticklabels(class_names)

    ax.set_ylabel('True label', size=14)
    ax.set_xlabel('Predicted label', size=14)

    if show:
        plt.show()
    else:
        return ax


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
        fmt = '{:,.0f}'

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


def _build_label_params_from_yvalue(y_value, absolute_distance_in_points):
    if y_value >= 0:
        #  If value of bar is positive: Place label above bar
        va = 'bottom'
        ytext = absolute_distance_in_points
    else:
        # If value of bar is negative: Place label below bar
        va = 'top'
        ytext = absolute_distance_in_points * -1

    return va, ytext


def _build_label_from_yvalue(y_value, integer_fmt, fmt):
    if isinstance(y_value, (int, np.integer)):
        label = integer_fmt.format(y_value)
    else:
        label = fmt.format(y_value)

    return label
