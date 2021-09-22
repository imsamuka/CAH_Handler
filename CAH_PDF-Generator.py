import CAH_Database

import argparse

from math import ceil

from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import simpleSplit

from reportlab.pdfbase.pdfmetrics import stringWidth

from reportlab.platypus import Table, TableStyle, Paragraph, SimpleDocTemplate, Image

def parseFloatTuple(string : str, unit = 1):
    l = string.strip()[1:-1].split(",")
    return (float(l[0])*unit, float(l[1])*unit)

def clamp(v, min, max):
    if v < min: return min
    if v > max: return max
    return v

# Changeable Areas -----------------------------

# ArgumentParser
parser = argparse.ArgumentParser(description='Read a ".txt" file of CAH_Database to generate a printable ".pdf" file.')
parser.add_argument('-i', '--input_file',  type=str, help='the ".txt" file you want to generate ".pdf" from')
parser.add_argument('-o', '--output_file', type=str, help='the output ".pdf" file. (optional)')
parser.add_argument('--pagesize', type=str, default="(210,297)", help="tuple of dimensions in mm (millimeter) of the page. Default is A4: (210,297)")
parser.add_argument('--cardsize', type=str, default="(50,50)",   help="tuple of dimensions in mm (millimeter) of the card. Default is (50,50)")
parser.add_argument('--margin', type=float, default=5.0,         help="size in mm (millimeter) of the margin. Default is 5")
parser.add_argument('--blackValue',     type=int, default=0,   help="the black from text and background. It ranges from 0 (black - default) to 255 (white)")
parser.add_argument('--gridBlackValue', type=int, default=150, help="the black from white cards grid. Default is 150. It ranges from 0 (black) to 255 (white)")
parser.add_argument('--normalfontsize', type=int, default=16,  help="normal text size. Default is 16")
parser.add_argument('--backfontsize',   type=int, default=22,  help="back of cards text size. Default is 22")
args = parser.parse_args()

INPUT_FILE  = args.input_file
OUTPUT_FILE = args.output_file

pagesize    = parseFloatTuple(args.pagesize, unit=mm)
cardWidth, cardHeight = parseFloatTuple(args.cardsize, unit=mm)
margin      = args.margin*mm

blackValue     = clamp(args.blackValue, 0, 255)
gridBlackValue = clamp(args.gridBlackValue, 0, 255)

fontsize     = args.normalfontsize
backfontsize = args.backfontsize

logoForWhite = "res/CAHLogo.png"
logoForBlack = "res/CAHLogoInverted.png"



# ----------------------------------------------

if not INPUT_FILE:
    INPUT_FILE = CAH_Database.dialogSelectInputFile()

# -------------------

if not INPUT_FILE:
    print('There is no input file!\n Insert one by adding a "--input_file" argument and then your file')
    exit(1)

if not OUTPUT_FILE:
    # Split the input file path by '/'
    path_list = INPUT_FILE.split("/")
    if "." in path_list[-1]:
        # Split the filename by '.' (extension)
        fn = path_list[-1].split(".", 1)
        path_list[-1] = fn[0] + ".pdf"
    else:
        path_list[-1] += ".pdf"
    OUTPUT_FILE = "/".join(path_list)
# ----------------------------------------------

# Get the cards list
wcList, bcList = CAH_Database.readTxtFile(INPUT_FILE)

# Invert page size if card is more wide than tall
if cardWidth > cardHeight and pagesize[1] > pagesize[0]:
    pagesize = (pagesize[1], pagesize[0])

cardXMargin = cardWidth*(3.5/50)
cardYMargin = cardXMargin*3/4

imgWidth  = cardWidth*3/4
imgHeight = imgWidth*(158/876)
imgTop = cardHeight - cardYMargin - imgHeight - 1.5*mm

textMaxWidth  = cardWidth  - (2*cardXMargin)
textMaxHeight = cardHeight - (2*cardYMargin) - imgHeight

col  = int((pagesize[0] - 2*margin) // cardWidth)
rows = int((pagesize[1] - 2*margin) // cardHeight)

wcExcess = len(wcList) % (col*rows)
bcExcess = len(bcList) % (col*rows)

ZZ = (0,0)
MM = (-1,-1)

# From Reportlab

img = Image(logoForWhite, imgWidth, imgHeight)

ps = ParagraphStyle(
    'title',
    fontName = 'Helvetica',
    fontSize = fontsize,
    leading = fontsize+2,
    splitLongWords = False
)

ts = TableStyle([
    ('VALIGN',      ZZ, MM, 'TOP'),
    ('LEFTPADDING', ZZ, MM, cardXMargin),
    ('RIGHTPADDING',ZZ, MM, cardXMargin),
    ('TOPPADDING',  ZZ, MM, cardYMargin)
])

cts = TableStyle([
    ('VALIGN',       ZZ, MM, 'TOP'),
    ('LEFTPADDING',  ZZ, MM, 0),
    ('RIGHTPADDING', ZZ, MM, 0),
    ('TOPPADDING',   ZZ, MM, 0),
    ('BOTTOMPADDING',ZZ, MM, 0)
])


ALL_tables = []


########################################################


def grayClr(v): return (v,v,v)


def setBlackColor(black_cards=False):
    global ps, ts, img
    # Depend on blackValue and gridBlackValue (Range 0-255)

    logo = logoForBlack if black_cards else logoForWhite
    tclr = grayClr(1 if black_cards else blackValue/255)
    bg   = grayClr(1 if not black_cards else blackValue/255)
    grid = grayClr(1 - gridBlackValue/255) if black_cards else grayClr(gridBlackValue/255)

    img = Image(logo, imgWidth, imgHeight)
    ps.textColor = tclr
    ts.add('BACKGROUND',ZZ,MM, bg)
    ts.add('GRID',ZZ,MM, 0.0000000000001, grid)


def reviseCPS(text, cps):

    # Split in Lines to check HEIGHT
    lines = simpleSplit(text, cps.fontName, cps.fontSize, textMaxWidth)

    # While height exceed the maxHeight - keeps shrinking text size
    while cps.leading * len(lines) > textMaxHeight:
        cps.fontSize -= 1
        cps.leading -= 0.6
        lines = simpleSplit(text, cps.fontName, cps.fontSize, textMaxWidth)

    # Search the line with the biggest width
    lines_width = [stringWidth(line, cps.fontName, cps.fontSize) for line in lines]
    biggest_line_index = lines_width.index(max(lines_width))
    biggest_line_width  = lines_width[biggest_line_index]
    biggest_line = lines[biggest_line_index]

    # While width exceed the maxWidth - keeps shrinking text size
    while biggest_line_width > textMaxWidth:
        cps.fontSize -= 1
        cps.leading -= 0.6
        biggest_line_width = stringWidth(biggest_line, cps.fontName, cps.fontSize)


def stringsToDT(strings):

    data_table = []

    for i in range(col*rows):

        # Try to get a string
        try: text = strings.pop(0)
        except: break

        # Clone the ParagraphStyle
        cps = ps.clone('')

        # Revise - change the text size it is too long
        reviseCPS(text, cps)

        # Tell me the SIZE if it Changes
        if cps.fontSize != ps.fontSize:
            print(f"Text Shortened (to {cps.fontSize}): {text}")

        # At the start of a column, append another list
        if i % col == 0: data_table.append([])

        # Create the table
        table = Table(
            [
                [Paragraph(text, cps)],
                [img]
            ],
            rowHeights = imgTop,
            style = cts
        )

        # Append the table in the current column list
        data_table[i//col].append(table)

    return data_table


def createBackDT(qtd):
    text = "Cards Against Humanity"
    cps = ps.clone('') # Clone the ParagraphStyle

    # Change the ParagraphStyle Clone
    cps.fontName = 'Helvetica-Bold'
    cps.fontSize = backfontsize
    cps.leading  = cps.fontSize+2

    reviseCPS(text, cps)

    data_table = []
    for i in range(qtd):
        if i % col == 0: data_table.append([])
        data_table[i//col].append(Paragraph(text, cps))
    return data_table


def appendDataTable(data_table, tables=ALL_tables, style=ts):

    # Must have at least a row and column - at least [[[]]]
    if not data_table or not data_table[0]: return

    # Create the data table
    table = Table(
        data_table,
        colWidths = cardWidth,
        rowHeights = cardHeight,
        style = style
    )

    # Append to tables list
    tables.append(table)


def fillExcessGap(excess, tables=ALL_tables):
    if excess <= 0: return

    # (1 + excess//col) -> How many rows the excess occupies
    gap_size = rows - (1 + excess//col)
    if gap_size <= 0: return

    filler_data_table = [[''] for i in range(gap_size)]
    appendDataTable(filler_data_table, tables=tables, style=None)


###################################################################


# ------- Get Back Cards Tables -------
setBlackColor(False)
appendDataTable(createBackDT(col*rows))
appendDataTable(createBackDT(wcExcess))
fillExcessGap(wcExcess)

setBlackColor(True)
appendDataTable(createBackDT(col*rows))
appendDataTable(createBackDT(bcExcess))
fillExcessGap(bcExcess)


# ------- Get White Cards Tables -------
setBlackColor(False)
while wcList: appendDataTable(stringsToDT(wcList))
fillExcessGap(wcExcess)

# ------- Get Black Cards Tables -------
setBlackColor(True)
CAH_Database.repeatOnList(bcList, '_', 3)
while bcList: appendDataTable(stringsToDT(bcList))
fillExcessGap(bcExcess)

# --------------- GENERATE FINAL PDF ---------------

title="Cards Against Humanity - Customized"
author = "ImSamuka"

pdf = SimpleDocTemplate(
    OUTPUT_FILE,
    pagesize=pagesize,
    topMargin=margin, leftMargin=margin, bottomMargin=margin, rightMargin=margin,
    title=title, author=author, creator=author, producer=author
)
pdf.build(ALL_tables)