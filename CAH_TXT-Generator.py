import CAH_Database
import argparse

from tkinter import filedialog
import tkinter
import os, sys

# ArgumentParser ------------------
parser = argparse.ArgumentParser(description='Rewritte a .txt file of CAH_Database to be a little prettier :D')
parser.add_argument('--input_file',  type=str, help='the .txt file you want rewritten')
parser.add_argument('--output_file', type=str, default='', help='the output file. (optional)')
parser.add_argument('--language',    type=str, default='', help='language of information. Default is ENG but currently can accept "pt-br" too.')
args = parser.parse_args()

INPUT_FILE = args.input_file
OUTPUT_FILE = args.output_file
LANG = args.language.lower()
# ----------------------------------

if LANG == 'pt-br' or LANG == 'br':
    fmt = "-formatado"
    winfs = "Cada linha a partir daqui vai ser considerado uma CARTA BRANCA"
    binfs = "Cada linha a partir daqui vai ser considerado uma CARTA PRETA"
else:
    fmt = "-formatted"
    winfs = "Each line from here will be considered a WHITE CARD"
    binfs = "Each line from here will be considered a BLACK CARD"

winfs = ["\n", CAH_Database.COMMENT_CHAR + winfs + "\n"]
binfs = ["\n", CAH_Database.COMMENT_CHAR + binfs + "\n"]


# ----------------------------------------------
UseDialogBoxes = True

if UseDialogBoxes and not INPUT_FILE:
    root = tkinter.Tk()
    root.withdraw()

    if sys.platform.startswith("linux"):
        initialdir = os.environ['HOME']
    elif sys.platform.startswith("win32") or sys.platform.startswith("cygwin"):
        initialdir = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')

    INPUT_FILE = filedialog.askopenfilename(
        parent = root,
        initialdir=initialdir,
        title='Select file',
        filetypes = (("TXT files","*.txt") , )
    )

# -------------------

assert not not INPUT_FILE , 'There is no input file! Insert one by adding a "--input_file" argument and then your file'

if not OUTPUT_FILE:
    # Split the input file path by '/'
    path_list = INPUT_FILE.split("/")
    if "." in path_list[-1]:
        # Split the filename by '.' (extension)
        fn = path_list[-1].split(".", 1)
        path_list[-1] = fn[0] + fmt + "." + fn[1]
    else:
        path_list[-1] += fmt
    OUTPUT_FILE = "/".join(path_list)

# ----------------------------------------------

wcList, bcList = CAH_Database.readTxtFile(INPUT_FILE)
tempList = []

# --------- Creating a formated new File --------------

try:
    newFile = open(OUTPUT_FILE, "w", encoding="utf-8")
except IOError:
    print("Error: Couldn't open file to write")
    exit(1)

# -------- White Cards

tempList = [i+"\n" for i in wcList]
tempList[-1] = str(tempList[-1])[:-1]
tempList = winfs + tempList
tempList.insert(0,CAH_Database.WC_MARK)
newFile.writelines(tempList)

# -------- Black Cards

tempList = [i+"\n" for i in bcList]
tempList[-1] = str(tempList[-1])[:-1]
tempList = binfs + tempList
tempList.insert(0,"\n"*5 + CAH_Database.BC_MARK)
newFile.writelines(tempList)