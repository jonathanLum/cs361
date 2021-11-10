import window as w
import graph as g
import re as re
import copy
import json
import requests
from requests.structures import CaseInsensitiveDict
import PySimpleGUI as sg
from matplotlib.ticker import NullFormatter  # useful for `logit` scale
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
matplotlib.use('TkAgg')


#### REQUEST INFO ####
url = "http://127.0.0.1:5000/"  # URL of locally run server
data = []
for key in w.englishText:
    for string in w.englishText[key]:
        data.append(string)



#### REGEX TESTS ####
floatReg = "[+-]?([0-9]*[.])?[0-9]+"


#### FUNCTIONS ####


def updateVisRows(entry=None, add=None):
    if entry is None and add is None:
        for i in range(w.entryLimit):
            rows = len(g.data[i][0])+1
            if rows < 2:
                rows = 2
            elif rows > w.inputsLimit:
                rows = w.inputsLimit
            for n in range(rows):
                window[w.ENTRY_KEY + f"{i+1}-ROW{n}-"].update(visible=True)
    elif entry is not None and add is not None:
        if add:
            window[w.ENTRY_KEY + f"{entry}-ROW{len(g.data[entry-1][0])}-"].update(visible=True)
        else:
            window[w.ENTRY_KEY + f"{entry}-ROW{len(g.data[entry-1][0])+1}-"].update(visible=False)


def setupWindow():
    window.maximize()
    window[w.ENTRY_KEY + "1-PIN-"].update(visible=True)
    updateVisRows()
    window["-NAME-"].expand(True, False, False)
    window["-SPACER-"].expand(True, True, False)

    # PLACEHOLDER TITLE AND HEADERS
    window[w.SEC1_KEY+"-TITLEIN-"].update(value=g.variables['title'])
    window[w.SEC1_KEY+"-XHEADER-"].update(value=g.variables['xlabel'])
    window[w.SEC1_KEY+"-YHEADER-"].update(value=g.variables['ylabel'])
    # PLACEHOLDER INPUTS
    for i in range(w.inputsMin-1):
        window[w.ENTRY_KEY+f"1-X{i}-"].update(value=str(g.data[0][0][i]))
        window[w.ENTRY_KEY+f"1-Y{i}-"].update(value=str(g.data[0][1][i]))

    # CHANGE CURSOR OVER CLICKABLE
    window["-LANGUAGE-"].set_cursor("hand2")
    window["-FORMAT-"].set_cursor("hand2")
    window["-OUTPUT-"].set_cursor("hand2")
    window['-SAVE-'].set_cursor("hand2")
    window[w.SEC1_KEY+"-TITLE-"].set_cursor("hand2")
    window[w.SEC1_KEY+"-BUTTON-"].set_cursor("hand2")
    window[w.SEC2_KEY+"-TITLE-"].set_cursor("hand2")
    window[w.SEC2_KEY+"-BUTTON-"].set_cursor("hand2")
    for i in range(w.entryLimit):
        window[f"-ENTRY{i+1}-TITLE-"].set_cursor("hand2")
        window[f"-ENTRY{i+1}-BUTTON-"].set_cursor("hand2")
    window['-ADDENTRY-'].set_cursor("hand2")
    window['-SUBENTRY-'].set_cursor("hand2")
    window["-CLEAR-"].set_cursor("hand2")

    g.variables['window'] = window
    g.updateGraph(w.entryCount)


def updateAllText():
    form = ""
    window["-lang-"].update(w.text["lang"][0] + ":")
    window["-LANGUAGE-"].set_tooltip(w.text["tips"][0])
    window["-format-0-"].update(w.text["format"][0] + ":")
    if values["-FORMAT-"] == w.formatOptions[0]:
        w.formatOptions = [w.text["format"][1], w.text["format"][2], w.text["format"][3]]
        form = w.formatOptions[0]
    elif values["-FORMAT-"] == w.formatOptions[1]:
        w.formatOptions = [w.text["format"][1], w.text["format"][2], w.text["format"][3]]
        form = w.formatOptions[1]
    elif values["-FORMAT-"] == w.formatOptions[2]:
        w.formatOptions = [w.text["format"][1], w.text["format"][2], w.text["format"][3]]
        form = w.formatOptions[2]
    window["-FORMAT-"].update(value=form, values=w.formatOptions)
    window["-FORMAT-"].set_tooltip(w.text["tips"][1])
    window["-output-"].update(w.text["output"][0] + ":")
    window["-OUTPUT-"].set_tooltip(w.text["tips"][2])
    window["-SAVE-"].update(w.text["save"][0])
    window["-SAVE-"].set_tooltip(w.text["tips"][3])
    window["-data-"].update(w.text["data"][0])
    window[w.SEC1_KEY+"-TITLE-"].update(w.text["tandh"][0])
    window["-tandh-1-"].update(w.text["tandh"][1])
    window["-tandh-2-"].update("X " + w.text["tandh"][2])
    window["-tandh-2-1"].update("Y " + w.text["tandh"][2])
    window[w.SEC2_KEY+"-TITLE-"].update(w.text["style"][0])
    window["-style-1-"].update(w.text["style"][1])
    window["-style-2-"].update(w.text["style"][2])
    window["-style-3-"].update(w.text["style"][3])
    for i in range(w.entryLimit):
        window[f"-ENTRY{i+1}-TITLE-"].update(w.text["entry"][0] + f" {i+1}")
        window[f"-ENTRY{i + 1}-LABEL-T"].update(w.text['style'][4] + ":")
        window[f"-ENTRY{i + 1}-COLOR-T"].update(w.text['style'][3] + ":")
    window["-ADDENTRY-"].update(w.text["entry"][1])
    window["-ADDENTRY-"].set_tooltip(w.text["tips"][4])
    window["-SUBENTRY-"].update(w.text["entry"][2])
    window["-SUBENTRY-"].set_tooltip(w.text["tips"][5])
    window["-CLEAR-"].update(w.text["clear"][0])
    window["-CLEAR-"].set_tooltip(w.text["tips"][6])


window = w.createWindow()
setupWindow()

while True:             # Event Loop
    event, values = window.read()
    #print(event, values)
    if event == sg.WIN_CLOSED or event == 'Exit':
        break

    if event == "-ADDENTRY-" and w.entryCount < w.entryLimit:
        w.entryCount += 1
        g.variables['entrycount'] = w.entryCount
        #   ENTRY SHOW
        window[w.ENTRY_KEY + str(w.entryCount)+"-PIN-"].update(visible=True)
        window["-SUBENTRY-"].update(visible=True)
        #   HIDE BUTTON WHEN FULL
        if w.entryCount == w.entryLimit:
            window["-ADDENTRY-"].update(visible=False)
        window.refresh()
        g.updateGraph(False)

    if event == "-SUBENTRY-" and w.entryCount > 1:
        #   ENTRY HIDE
        window[w.ENTRY_KEY + str(w.entryCount)+"-PIN-"].update(visible=False)
        window["-ADDENTRY-"].update(visible=True)
        w.entryCount -= 1
        g.variables['entrycount'] = w.entryCount
        #   HIDE BUTTON WHEN EMPTY
        if w.entryCount == 1:
            window["-SUBENTRY-"].update(visible=False)
        window.refresh()
        g.updateGraph(False)


    if event.startswith(w.SEC1_KEY):
        if event == w.SEC1_KEY+"-TITLEIN-":
            g.variables['title'] = values[w.SEC1_KEY+"-TITLEIN-"]
            g.updateGraph(False)
        elif event == w.SEC1_KEY+"-XHEADER-":
            g.variables['xlabel'] = values[w.SEC1_KEY+"-XHEADER-"]
            g.updateGraph(False)
        elif event == w.SEC1_KEY+"-YHEADER-":
            g.variables['ylabel'] = values[w.SEC1_KEY+"-YHEADER-"]
            g.updateGraph(False)
        else:
            #   SECTION COLLAPSE AND SHOW
            window[w.SEC1_KEY].update(visible=not window[w.SEC1_KEY].visible)
            #   ARROW IMAGE CHANGE
            window[w.SEC1_KEY+'-BUTTON-'].update(window[w.SEC1_KEY].metadata[1] if window[w.SEC1_KEY].visible else window[w.SEC1_KEY].metadata[0])

    if event.startswith(w.SEC2_KEY):
        if event == w.SEC2_KEY+"-LEGEND-":
            g.variables['legend'] = values[w.SEC2_KEY+"-LEGEND-"]
            g.updateGraph(False)
        elif event == w.SEC2_KEY+"-GRID-":
            g.variables['grid'] = values[w.SEC2_KEY+"-GRID-"]
            g.updateGraph(False)
        elif event == w.SEC2_KEY+"-COLOR-":
            g.variables['color'] = values[w.SEC2_KEY+"-COLOR-"]
            g.updateGraph(False)
        else:
            #   SECTION COLLAPSE AND SHOW
            window[w.SEC2_KEY].update(visible=not window[w.SEC2_KEY].visible)
            #   ARROW IMAGE CHANGE
            window[w.SEC2_KEY+'-BUTTON-'].update(window[w.SEC2_KEY].metadata[1] if window[w.SEC2_KEY].visible else window[w.SEC2_KEY].metadata[0])

    if event.startswith(w.ENTRY_KEY):
        entryNum = event[6]
        inputLetter = event[8] # X or Y
        inputNum = event[9] #and 10 for next digit
        validD = re.match(floatReg, event[10])
        if validD:
            inputNum += event[10]
        #print(inputLetter)
        #print(inputNum)
        # CHANGE IN STYLING
        if event.endswith("-LABEL-") or event.endswith("-COLOR-"):
            g.data[int(entryNum)-1][3] = values[f"{w.ENTRY_KEY}{entryNum}-LABEL-"]
            g.data[int(entryNum)-1][2] = values[f"{w.ENTRY_KEY}{entryNum}-COLOR-"]
            g.updateGraph(False)
            print(g.data)
        # CHANGE IN INPUTS
        elif inputLetter == "X" or inputLetter == "Y":
            userInputX = values[w.ENTRY_KEY+entryNum+f"-X{inputNum}-"]
            userInputY = values[w.ENTRY_KEY+entryNum+f"-Y{inputNum}-"]
            validX = re.match(floatReg, userInputX)
            validY = re.match(floatReg, userInputY)
            if validX and validY:
                if int(inputNum) == len(g.data[int(entryNum)-1][0]):
                    g.data[int(entryNum)-1][0].append(float(userInputX))
                    g.data[int(entryNum)-1][1].append(float(userInputY))
                else:
                    g.data[int(entryNum)-1][0][int(inputNum)] = float(userInputX)
                    g.data[int(entryNum)-1][1][int(inputNum)] = float(userInputY)
                #print(g.data)
                updateVisRows(int(entryNum), True)
                g.updateGraph(False)
            elif userInputX == "" and userInputY == "" and int(inputNum) == len(g.data[int(entryNum)-1][0])-1:
                #Remove row from data and update
                g.data[int(entryNum)-1][0].pop()
                g.data[int(entryNum)-1][1].pop()
                updateVisRows(int(entryNum), False)
                g.updateGraph(False)
        # CLICK ON BUTTON OR TITLE
        else:
            #   ENTRY COLLAPSE AND SHOW
            window[w.ENTRY_KEY + entryNum].update(visible=not window[w.ENTRY_KEY + entryNum].visible)
            #   ARROW IMAGE CHANGE
            window[w.ENTRY_KEY + entryNum + '-BUTTON-'].update(window[w.ENTRY_KEY + entryNum].metadata[1] if window[w.ENTRY_KEY + entryNum].visible else window[w.ENTRY_KEY + entryNum].metadata[0])

    if event == "-LANGUAGE-":
        if values["-LANGUAGE-"] == w.languageOptions[0]:
            w.text = copy.deepcopy(w.englishText)
        else:
            language = values["-LANGUAGE-"]
            dictToSend = {}
            for i in range(len(data)):
                dictToSend[i] = data[i]
            # You will need to serialize the dictionary to JSON before sending request.
            json_object = json.dumps(dictToSend, indent=1)
            # HOW TO FORMAT THE POST REQUEST....
            pop = sg.Window(w.text["tips"][8], [[sg.T(w.text["tips"][8])]], no_titlebar=True, keep_on_top=True, font=w.generalFont, finalize=True)
            pop.read(timeout=10)
            response = requests.post(url + "translateArray/" + language, json=json_object)
            # OVERWRITE TEXT
            textback = response.json()
            index = 0
            for key in w.englishText:
                for i in range(len(w.englishText[key])):
                    w.text[key][i] = textback[str(index)]
                    index += 1
            pop.close()
        updateAllText()
        window.Refresh()

    if event == "-FORMAT-":
        if values["-FORMAT-"] == w.formatOptions[0]:
            g.variables['format'] = "line"
        elif values["-FORMAT-"] == w.formatOptions[1]:
            g.variables['format'] = "bar"
        elif values["-FORMAT-"] == w.formatOptions[2]:
            g.variables['format'] = "point"
        g.updateGraph(False)

    if event == "-OUTPUT-":
        g.variables['output'] = values["-OUTPUT-"]

    if event == "-CLEAR-":
        choice = sg.popup_ok_cancel(w.text["tips"][7], no_titlebar=False, keep_on_top=True, grab_anywhere=True)
        if choice == "OK":
            # CLEAR GRAPH VARIABLES
            g.clearGraph()
            g.updateGraph(False)

            # CLEAR INPUTS
            window[w.SEC1_KEY + "-TITLEIN-"].update(value="")
            window[w.SEC1_KEY + "-XHEADER-"].update(value="")
            window[w.SEC1_KEY + "-YHEADER-"].update(value="")
            for i in range(w.entryLimit):
                for n in range(w.inputsLimit):
                    window[w.ENTRY_KEY + f"{i+1}" + f"-X{n}-"].update(value="")
                    window[w.ENTRY_KEY + f"{i+1}" + f"-Y{n}-"].update(value="")

    if event == "-FOLDER-":
        g.saveGraph(values["-FOLDER-"])


window.close()
