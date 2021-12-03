import PySimpleGUI as sg
import copy

# ADD A CLEAR BUTTON WITH ARE YOU SURE PROMPT
#### VARIABLES ####
#   TEXT
name = "Graphtastic"
englishText = {"lang": ["Language"],
               "format": ["Format", "Line", "Bar", "Point"],
               "output": ["Output"],
               "save": ["Save"],
               "data": ["Data Entry"],
               "tandh": ["Title and Headers", "Title", "Header"],
               "style": ["Style", "Legend", "Grid", "Color", "Label"],
               "entry": ["Entry", "Add New Entry", "Remove Entry"],
               "clear": ["Clear Graph"],
               "tips": ["Language: Changes program Language", "Format: Changes format of graph eg. Line vs Bar",
                        "Output: Changes image file type\n when save button is pressed", 'Save: Saves an image file\n of the created graph\n with file type of "Output"',
                        "Add a new Entry section (Max: 5)", "Remove last Entry section \n(Min: 1, will not delete entered data only disable)",
                        "Clear Graph: Will clear all Inputs", "Caution! This action cannot be undone", "Please Wait..."]}

text = copy.deepcopy(englishText)
languageOptions = ["English", "Spanish", "Japanese", 'afrikaans',
    'albanian',
    'belarusian',
    'catalan',
'czech',
'danish',
'dutch',
'filipino',
'finnish',
'french',
'german',
'greek',
'hawaiian',
'hebrew',
'hindi',
'hungarian',
'icelandic',
'indonesian',
'irish',
'italian',
'korean',
'latin',
'maori',
'mongolian',
'norwegian',
'polish',
'punjabi',
'romanian',
'russian',
'samoan',
'swahili',
'swedish',
'thai',
'turkish',
'ukrainian']
formatOptions = [text["format"][1], text["format"][2], text["format"][3]]
outputOptions = ["PNG", "JPG", "SVG"]

#   STYLING
logoImage = "logo.png"
iconImage = "logo.ico"
generalFont = "Helvitica 18 bold"
nameFont = "Helvitica 40 bold"
navSpace = 100
navFont = "Helvitica 25 bold"
inputFont = "Helvitica 14 bold"


#### FUNCTIONS ####
def createWindow():
    return sg.Window(name, layout, finalize=True, margins=(10, 10), font=generalFont, icon=iconImage)


def collapsible(layout, key, title='', arrows=(sg.SYMBOL_DOWN, sg.SYMBOL_UP), collapsed=False, vis=False):
    """
    User Defined Element
    A "collapsable section" element. Like a container element that can be collapsed and brought back
    :param layout:Tuple[List[sg.Element]]: The layout for the section
    :param key:Any: Key used to make this section visible / invisible
    :param title:str: Title to show next to arrow
    :param arrows:Tuple[str, str]: The strings to use to show the section is (Open, Closed).
    :param collapsed:bool: If True, then the section begins in a collapsed state
    :return:sg.Column: Column including the arrows, title and the layout that is pinned
    """
    return sg.Column([[sg.T((arrows[0] if collapsed else arrows[1]), enable_events=True, k=key+'-BUTTON-'),
                       sg.T(title, enable_events=True, key=key+'-TITLE-')],
                      [sg.pin(sg.Column(layout, key=key, visible=not collapsed, metadata=arrows))],
                     [sg.HSeparator()]], key=key+"-PIN-", visible=vis, pad=(0,0))


#### ALL LAYOUTS ####

### NAVBAR LAYOUT ###
navbar = [sg.Image(logoImage, subsample=5),
          sg.Text(name, font=nameFont, key="-NAME-"),
          sg.Text(text["lang"][0] + ":", font=navFont, key="-lang-"),
          sg.Combo(languageOptions, default_value=languageOptions[0], tooltip=text["tips"][0], key="-LANGUAGE-", font=navFont, enable_events=True),
          sg.Sizer(navSpace, 0),
          sg.Text(text["format"][0] + ":", font=navFont, key="-format-0-"),
          sg.Combo(formatOptions, default_value=formatOptions[0], tooltip=text["tips"][1], key="-FORMAT-", font=navFont, enable_events=True),
          sg.Sizer(navSpace, 0),
          sg.Text(text["output"][0] + ":", font=navFont, key="-output-"),
          sg.Combo(outputOptions, default_value=outputOptions[0], tooltip=text["tips"][2], key="-OUTPUT-", font=navFont, enable_events=True),
          sg.Input(visible=False, key="-FOLDER-", enable_events=True),
          sg.FolderBrowse(text["save"][0], pad=(100, 0), tooltip=text["tips"][3], key="-SAVE-", font=navFont)]


### DATA COLUMN LAYOUT ###
#   TITLES AND HEADERS SECTION
SEC1_KEY = '-TITLEANDHEAD'
titlesec = [[sg.Text(text["tandh"][1], key="-tandh-1-")],
            [sg.Input(key=SEC1_KEY+"-TITLEIN-", size=(40,1), enable_events=True)],
            [sg.Text("X " + text["tandh"][2], key="-tandh-2-")],
            [sg.Input(key=SEC1_KEY+"-XHEADER-", size=(40,1), enable_events=True)],
            [sg.Text("Y " + text["tandh"][2], key="-tandh-2-1")],
            [sg.Input(key=SEC1_KEY+"-YHEADER-", size=(40,1), enable_events=True)]]

#   GENERAL STYLE SECTION
SEC2_KEY = '-STYLE'
stylesec = [[sg.Text(f"{text['style'][1]}:", key="-style-1-"), sg.CB("", key=SEC2_KEY+"-LEGEND-", size=(5,5), enable_events=True)],
            [sg.Text(f"{text['style'][2]}:", key="-style-2-"), sg.CB("", key=SEC2_KEY+"-GRID-", size=(5,5), enable_events=True)],
            [sg.Text(text['style'][3], key="-style-3-")],
            [sg.Input(key=SEC2_KEY+"-COLOR-", size=(40,1), enable_events=False)]]


##   WHOLE DATA COLUMN  ##
datacol = [[sg.Text(text["data"][0], key="-data-", pad=(200, 0), font=navFont, justification="center")],
           [sg.HSeparator()],
           #    Section 1 part
           [collapsible(titlesec, SEC1_KEY,  text["tandh"][0], collapsed=True, vis=True)],
           [collapsible(stylesec, SEC2_KEY,  text["style"][0], collapsed=True, vis=True)]]

#   ENTRY SECTION
ENTRY_KEY = '-ENTRY'
inputsLimit = 15
inputsCount = 5
inputsMin = 5
entryLimit = 5
entryCount = 1
# CREATE ENTRIES AND ADD TO DATA COLUMN
for i in range(entryLimit):
    entryKey = ENTRY_KEY + f"{i+1}"
    entries = [[sg.Text(f"{text['style'][4]}:", key=f"{entryKey}-LABEL-T"), sg.Input(key=f"{entryKey}-LABEL-", font=inputFont, size=(12, 1), enable_events=True),
                sg.Text(f"{text['style'][3]}:", key=f"{entryKey}-COLOR-T"), sg.Input(key=f"{entryKey}-COLOR-", font=inputFont, size=(12, 1), enable_events=True)]]

    entries += [[sg.pin(sg.Column([[sg.Text(f"{i+1}.  X: ", font=inputFont), sg.Input(key=entryKey + f"-X{i}-", font=inputFont, size=(12, 1), enable_events=True),
                sg.Text("Y: ", font=inputFont), sg.Input(key=entryKey + f"-Y{i}-", font=inputFont, size=(12, 1), enable_events=True)]], key=entryKey + f"-ROW{i}-", visible=False))] for i in range(inputsLimit)]

    datacol += [sg.pin(collapsible(entries, entryKey,  text["entry"][0] + f" {i+1}", collapsed=True))],
# ADD ENTRY AND CLEAR BUTTONS TO DATA COLUMN
datacol += [
            [sg.pin(sg.Button(text["entry"][1], tooltip=text["tips"][4], key="-ADDENTRY-", pad=(50, 0))),
             sg.pin(sg.Button(text["entry"][2], tooltip=text["tips"][5], key="-SUBENTRY-", visible=False, pad=(50, 0)))],
            [sg.Sizer(0, 30)],
            [sg.Column([[sg.Button(text["clear"][0], tooltip=text["tips"][6], key="-CLEAR-")]], expand_x=True, element_justification="center")],
            [sg.Text("", key="-SPACER-", size=(20, 80))]
           ]


### GRAPH COLUMN LAYOUT ###
graphcol = [[sg.Canvas(key='-CANVAS-')]]


### FULL LAYOUT ###
layout = [
    [
        navbar,
        sg.Column(datacol, element_justification='left'),
        sg.VSeparator(),
        sg.Column(graphcol)
    ]
]

