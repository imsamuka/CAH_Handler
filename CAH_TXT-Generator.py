import CAH_Database
import argparse

from tkinter import filedialog
import tkinter
import os

# ArgumentParser ------------------
parser = argparse.ArgumentParser(description='Rewritte a .txt file of CAH_Database to be a little prettier :D')
parser.add_argument('--input_file',  type=str, help='the .txt file you want rewritten')
parser.add_argument('--output_file', type=str, default='', help='the output file. (optional)')
parser.add_argument('--language',    type=str, default='', help='language of information. Default is ENG but currently can accept 'pt-br' too.')
args = parser.parse_args()

INPUT_FILE = args.input_file
OUTPUT_FILE = args.output_file
LANG = args.language
# ----------------------------------

if LANG.lower() == 'pt-br' or LANG.lower() == 'br':
    fmt = "Formatado - "
    winfs = "Cada linha a partir daqui vai ser considerado uma CARTA BRANCA"
    binfs = "Cada linha a partir daqui vai ser considerado uma CARTA PRETA"
else:
    fmt = "Formatted - "
    winfs = "Each line from here will be considered a WHITE CARD"
    binfs = "Each line from here will be considered a BLACK CARD"

winfs = ["\n", CAH_Database.COMMENT_CHAR + winfs + "\n"]
binfs = ["\n", CAH_Database.COMMENT_CHAR + binfs + "\n"]


# ----------------------------------------------
UseDialogBoxes = True

if UseDialogBoxes and INPUT_FILE == None:
    root = tkinter.Tk()
    root.withdraw()
    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    INPUT_FILE = filedialog.askopenfilename(parent = root,initialdir=desktop,title='Select file',  filetypes = (("TXT files","*.txt") , )    )

# -------------------

assert INPUT_FILE != None , 'There is no input file! Insert one by adding a "--input_file" argument and then your file'

if not len(OUTPUT_FILE) >= 1:
    if "/" in INPUT_FILE:
        OUTPUT_FILE = INPUT_FILE.split("/")
        OUTPUT_FILE[-1] = fmt+OUTPUT_FILE[-1]
        OUTPUT_FILE = "/".join(OUTPUT_FILE)
    else:
        OUTPUT_FILE = fmt+INPUT_FILE

# ----------------------------------------------

wcList, bcList = CAH_Database.readTxtFile(INPUT_FILE)
tempList = []

# --------- Creating a formated new File --------------
newFile = open(OUTPUT_FILE,"w")

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