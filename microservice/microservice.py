from matplotlib.ticker import NullFormatter  # useful for `logit` scale
import matplotlib.pyplot as plt
import matplotlib
import numpy as np


#### VARIABLES ####
X = 0
Y = 1
COLOR = 2
NAME = 3


variables = {'size': (8, 5),
             'dpi': 200,
             'format': "line",
             'output': "PNG",
             'filename': "graph",
             'title': "",
             'xlabel': "",
             'ylabel': "",
             'legend': False,
             'grid': False,
             'color': "white",
             'entries': [[[], [], "", ""],
                         [[], [], "", ""],
                         [[], [], "", ""],
                         [[], [], "", ""],
                         [[], [], "", ""]]
             }


def plotGraph():
    # PLOT BASED ON FORMAT
    if variables['format'] == "line":
        for i in range(len(variables['entries'])):
            plt.plot(variables['entries'][i][X], variables['entries'][i][Y],
                     color=variables['entries'][i][COLOR] if variables['entries'][i][COLOR] != "" else "k",
                     label=variables['entries'][i][NAME], marker="o")
    elif variables['format'] == "bar":
        spc = np.arange(len(variables['entries'][0][X]))
        barW = 1 / (len(variables['entries']) + 1)
        for i in range(len(variables['entries'])):
            if variables['entries'][i][Y] == []:
                continue
            plt.bar(spc + (i * barW), variables['entries'][i][Y], width=barW,
                    color=variables['entries'][i][COLOR] if variables['entries'][i][COLOR] != "" else "lightblue",
                    edgecolor="k", align='edge', label=variables['entries'][i][NAME])
        plt.xticks(spc + ((len(variables['entries'])) * barW) / 2, variables['entries'][0][X])
    elif variables['format'] == "point":
        for i in range(len(variables['entries'])):
            plt.plot(variables['entries'][i][X], variables['entries'][i][Y], ".",
                     color=variables['entries'][i][COLOR] if variables['entries'][i][COLOR] != "" else "k",
                     label=variables['entries'][i][NAME])


def styleGraph(fig):
    plt.title(variables['title'])
    plt.xlabel(variables['xlabel'])
    plt.ylabel(variables['ylabel'])
    if variables['legend']:
        plt.legend(loc=0)
    if variables['grid']:
        if variables['format'] == "bar":
            plt.grid(True, color="0.5", axis="y", dashes=(5, 2, 1, 2))
        else:
            plt.grid(True, color="0.5", dashes=(5, 2, 1, 2))
    else:
        plt.grid(False)
    if variables['color'] != "":
        fig.set_facecolor(variables['color'])


def drawGraph():
    # make fig and plot
    fig = plt.figure(figsize=variables['size'], dpi=variables['dpi'])

    plotGraph()

    styleGraph(fig)

    # SAVE FILE
    fig.savefig(f"graph.{variables['output']}")

    # RETURN FILENAME
    return f"graph.{variables['output']}"
