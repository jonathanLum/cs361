from matplotlib.ticker import NullFormatter  # useful for `logit` scale
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
import numpy as np
matplotlib.use('TkAgg')

#### VARIABLES ####
X = 0
Y = 1
COLOR = 2
NAME = 3

data = [[[1,2,3,4], [3,4,8,9], "k", "My Line"],
        [[], [], "g", ""],
        [[], [], "r", ""],
        [[], [], "b", ""],
        [[], [], "m", ""]]

variables = {'fig': False,
             'size': (8, 5),
             'dpi': 200,
             'format': "line",
             'output': "PNG",
             'title': "Title",
             'xlabel': "X Axis",
             'ylabel': "Y Axis",
             'legend': False,
             'grid': False,
             'color': "white",
             'entrycount': 1
             }


def setupGraph():
    fig = plt.figure(figsize=variables['size'], dpi=variables['dpi'])
    variables['fig'] = fig


def plotGraph():
    # PLOT BASED ON FORMAT
    if variables['format'] == "line":
        for i in range(variables['entrycount']):
            plt.plot(data[i][X], data[i][Y], color=data[i][COLOR] if data[i][COLOR] != "" else "k", label=data[i][NAME],
                     marker="o")
    elif variables['format'] == "bar":
        spc = np.arange(len(data[0][X]))
        barW = 1 / (variables['entrycount'] + 1)
        for i in range(variables['entrycount']):
            if not data[i][Y]:
                continue
            plt.bar(spc + (i * barW), data[i][Y], width=barW,
                    color=data[i][COLOR] if data[i][COLOR] != "" else "lightblue", edgecolor="k", align='edge',
                    label=data[i][NAME])
        plt.xticks(spc + ((variables['entrycount']) * barW) / 2, data[0][X])
    elif variables['format'] == "point":
        for i in range(variables['entrycount']):
            plt.plot(data[i][X], data[i][Y], ".", color=data[i][COLOR] if data[i][COLOR] != "" else "k",
                     label=data[i][NAME])


def styleGraph():
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
        variables['fig'].set_facecolor(variables['color'])


def drawGraph():
    plotGraph()
    styleGraph()
    return variables['fig']


def updateGraph(new=True):
    if not new:
        variables['fig_agg'].get_tk_widget().forget()
        plt.clf()
    variables['fig_agg'] = renderFigure(variables['window']['-CANVAS-'].TKCanvas, drawGraph())


def clearGraph():
    global data
    data = [[[], [], "k", ""],
              [[], [], "g", ""],
              [[], [], "r", ""],
              [[], [], "b", ""],
              [[], [], "m", ""]]
    variables['title'] = ""
    variables['xlabel'] = ""
    variables['ylabel'] = ""


def renderFigure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg


def saveGraph(loc):
    tempTitle = variables['title']
    if tempTitle == "":
        tempTitle = "MyGraph"
    if loc != "":
        variables['fig'].savefig(f"{loc}/{tempTitle}.{variables['output']}")

