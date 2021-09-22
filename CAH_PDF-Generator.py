import CAH_Database

import argparse

from math import ceil

from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import simpleSplit

from reportlab.pdfbase.pdfmetrics import stringWidth

from reportlab.platypus import Table, TableStyle, Paragraph, SimpleDocTemplate, Image

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
parser.add_argument('--blackValue',       type=int, default=0,   help="the black from text and background. It ranges from 0 (black - default) to 255 (white)")
parser.add_argument('--gridBlackValue',   type=int, default=150, help="the black from white cards grid. Default is 150. It ranges from 0 (black) to 255 (white)")
parser.add_argument('--normalfontsize',   type=int, default=16,  help="normal text size. Default is 16")
parser.add_argument('--backlogofontsize', type=int, default=22,  help="back of cards text size. Default is 22")
args = parser.parse_args()

INPUT_FILE  = args.input_file
OUTPUT_FILE = args.output_file
pagesize    = args.pagesize
cardWidth   = mm*float(args.cardsize[1:-1].split(",")[0])
cardHeight  = mm*float(args.cardsize[1:-1].split(",")[1])
margin      = mm*args.margin
blackValue  = clamp(args.blackValue, 0, 255)
gridBlackValue = clamp(args.gridBlackValue, 0, 255)
fontSize = args.normalfontsize
backlogofontsize = args.backlogofontsize

logoForWhite = "res/CAHLogo.png"
logoForBlack = "res/CAHLogoInverted.png"



# ----------------------------------------------
UseDialogBoxes = True

if UseDialogBoxes and not INPUT_FILE:
    INPUT_FILE = dialogSelectInputFile()

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

pagesize = tuple(pagesize[1:-1].split(","))
pagesize = (float(pagesize[0])*mm,float(pagesize[1])*mm)

# Invert page size if card is more wide than tall
if cardWidth > cardHeight and pagesize[1] > pagesize[0]:
    pagesize = (pagesize[1], pagesize[0])

cellMargin = cardWidth*(3.5/50)
cellTop    = cellMargin*3/4

imgWidth  = cardWidth*3/4
imgHeight = imgWidth*(158/876)

cellAboveImageHeight = cardHeight - cellTop - imgHeight - 1.5*mm

maxWidth  = cardWidth  - (2*cellMargin)
maxHeight = cardHeight - (2*cellMargin*3/4) - imgHeight

col  = int((pagesize[0] - 2*margin) // cardWidth)
rows = int((pagesize[1] - 2*margin) // cardHeight)

wcExcess = len(wcList) % (col*rows)
bcExcess = len(bcList) % (col*rows)

# From Reportlab

img = Image(logoForWhite, imgWidth, imgHeight)

ps = ParagraphStyle(
    'title',
    fontName = 'Helvetica',
    fontSize = fontSize,
    leading = fontSize+2,
    splitLongWords = False
)

ts = TableStyle([
    ('VALIGN',      (0,0), (-1,-1), 'TOP'),
    ('LEFTPADDING', (0,0), (-1,-1), cellMargin),
    ('RIGHTPADDING',(0,0), (-1,-1), cellMargin),
    ('TOPPADDING',  (0,0), (-1,-1), cellTop)
])

cts = TableStyle([
    ('VALIGN',       (0,0), (-1,-1), 'TOP'),
    ('LEFTPADDING',  (0,0), (-1,-1), 0),
    ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ('TOPPADDING',   (0,0), (-1,-1), 0),
    ('BOTTOMPADDING',(0,0), (-1,-1), 0)
])


ALL_tables = []


########################################################


def grayClr(v): return (v,v,v)


def setColors(SetBlackCards=False):
    global ps, ts, img
    # Depend on blackValue and gridBlackValue (Range 0-255)
    if not SetBlackCards:
        # WhiteCards
        img = Image(logoForWhite, imgWidth, imgHeight)
        ps.textColor = grayClr(blackValue/255)
        ts.add('BACKGROUND',(0,0),(-1,-1), grayClr(1))
        ts.add('GRID',(0,0),(-1,-1), 0.0000000000001, grayClr(gridBlackValue/255))
    else:
        # BlackCards
        img = Image(logoForBlack, imgWidth, imgHeight)
        ps.textColor = grayClr(1)
        ts.add('BACKGROUND', (0,0), (-1,-1), grayClr(blackValue/255))
        ts.add('GRID', (0,0), (-1,-1), 0.0000000000001, grayClr(1 - gridBlackValue/255))


def reviseCPS(text, cps):

    # Split in Lines to check HEIGHT
    lines = simpleSplit(text, cps.fontName, cps.fontSize, maxWidth)

    while cps.leading * len(lines) > maxHeight:
        cps.fontSize -= 1
        cps.leading -= 0.6
        lines = simpleSplit(text, cps.fontName, cps.fontSize, maxWidth)

    # Get Lines WIDTH
    lineWidth = [stringWidth(k, cps.fontName, cps.fontSize) for k in lines]

    # Search the line with the biggest width
    k         = lines[    lineWidth.index(max(lineWidth))]
    lineWidth = lineWidth[lineWidth.index(max(lineWidth))]

    while lineWidth > maxWidth:
        cps.fontSize -= 1
        cps.leading -= 0.6
        lineWidth = stringWidth(k, cps.fontName, cps.fontSize)


def getData(List):

    data = []

    for i in range(col*rows):

        # Try to get a string
        try: text = List.pop(0)
        except: break

        # Clone the ParagraphStyle
        cps = ps.clone('')

        # Revise - change the text size it is too long
        reviseCPS(text, cps)

        # Tell me the SIZE if it Changes
        if cps.fontSize != ps.fontSize:
            print(f"Text Shortened (to {cps.fontSize}): {text}")

        # At the start of a column, append another list
        if i % col == 0: data.append([])

        # Create the table
        table = Table(
            [
                [Paragraph(text, cps)],
                [img]
            ],
            rowHeights = cellAboveImageHeight,
            style = cts
        )

        # Append the table in the current column list
        data[i//col].append(table)

    return data


def getBackTb(qtd):
    text = "Cards Against Humanity"
    cps = ps.clone('') # Clone the ParagraphStyle

    # Change the ParagraphStyle Clone
    cps.fontName = 'Helvetica-Bold'
    cps.fontSize = backlogofontsize
    cps.leading  = cps.fontSize+2

    reviseCPS(text, cps)

    data = []
    for i in range(qtd):
        if i % col == 0: data.append([])
        data[i//col].append(Paragraph(text, cps))
    return data


def fillExcessGap(excess, tables):
    if excess <= 0: return

    # (1 + excess//col) -> How many rows the excess occupies
    gap_size = rows - (1 + excess//col)
    if gap_size <= 0: return

    fillers = [[''] for i in range(gap_size)]
    table = Table(fillers, cardWidth, cardHeight)
    tables.append(table)


###################################################################


# ------- Get Back Cards Tables -------
setColors()
ALL_tables.append(Table(getBackTb(col*rows), cardWidth, cardHeight, style=ts))
if wcExcess: ALL_tables.append(Table(getBackTb(wcExcess), cardWidth, cardHeight, style=ts))
fillExcessGap(wcExcess, ALL_tables)

setColors(True)
ALL_tables.append(Table(getBackTb(col*rows), cardWidth, cardHeight,style=ts))
if bcExcess: ALL_tables.append(Table(getBackTb(bcExcess), cardWidth, cardHeight,style=ts))
fillExcessGap(bcExcess, ALL_tables)


# ------- Get White Cards Tables -------
setColors()
while wcList:
    table = Table(getData(wcList), cardWidth, cardHeight, style=ts)
    ALL_tables.append(table)
fillExcessGap(wcExcess, ALL_tables)

# ------- Get Black Cards Tables -------
setColors(True)

CAH_Database.repeatOnList(bcList, '_', 3)

while bcList:
    table = Table(getData(bcList), cardWidth, cardHeight, style=ts)
    ALL_tables.append(table)
fillExcessGap(bcExcess, ALL_tables)

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