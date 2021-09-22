import CAH_Database
import argparse


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
    winfs = " Cada linha a partir daqui vai ser considerado uma CARTA BRANCA"
    binfs = " Cada linha a partir daqui vai ser considerado uma CARTA PRETA"
else:
    fmt = "-formatted"
    winfs = " Each line from here will be considered a WHITE CARD"
    binfs = " Each line from here will be considered a BLACK CARD"

# ----------------------------------------------
UseDialogBoxes = True

if UseDialogBoxes and not INPUT_FILE:
    INPUT_FILE = CAH_Database.dialogSelectInputFile()

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

cards = CAH_Database.readTxtFile(INPUT_FILE)
infos = (winfs, binfs)
CAH_Database.writeTxtFile(OUTPUT_FILE, cards, infos)