# ----------------------------------------------------------------------------------------------------------------------
# EZ Plot Library
# ----------------------------------------------------------------------------------------------------------------------

# imports
from matplotlib import pyplot
import numpy as np


def create_bar_graph(x_data, y_data, x_lab='x', y_lab='y', title='title', show=False):
    """
    Creates a bar graph from provided data.

    :param list x_data: Data for the x-axis.
    :param list y_data: Data for the y-axis.
    :param str x_lab: Label for the x-axis.
    :param str y_lab: Label for the y-axis.
    :param str title: Title of the plot.
    :param bool show: Indicates if the graph should be displayed.
    """

    fig, ax = pyplot.subplots(figsize=(8, 4))
    rects = ax.bar(x_data, y_data, width=0.6)
    ax.set_xlabel(x_lab)
    ax.set_ylabel(y_lab)
    ax.set_title(title)
    ax.set_ylim((0, np.max(y_data) + np.sqrt(np.max(y_data))))
    pyplot.tick_params('x', labelsize=8, labelrotation=45, direction='out')
    for rect in rects:
        height = int(rect.get_height())
        if height >= 5:
            yloc = -15
            color = 'white'
        else:
            yloc = 8
            color = 'black'
        ax.annotate(str(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, yloc),
                    textcoords="offset points",
                    ha='center',
                    va='center',
                    color=color,
                    weight='bold',
                    fontsize='large')
    pyplot.tight_layout()
    if show:
        pyplot.show()
# ----------------------------------------------------------------------------------------------------------------------
# End
# ----------------------------------------------------------------------------------------------------------------------
