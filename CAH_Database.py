# Constants
WC_MARK = "[WHITECARDS]"
BC_MARK = "[BLACKCARDS]"
BC_BLANK_CHAR = "_"
COMMENT_CHAR = "#"

# Functions

def unifyOnList(strings : list[str], char : str) -> None:
    dchar = char+char
    for i in range(len(strings)):
        while dchar in strings[i]:
            strings[i] = strings[i].replace(dchar,char)

def repeatOnList(strings : list[str], char : str, n : int) -> None:
    nchar = char*n
    for i in range(len(strings)):
        if char in strings[i]:
            strings[i] = strings[i].replace(char,nchar)

def readTxtFile(filepath : str) -> tuple[list[str], list[str]]:
    IGNORE_CHARS = COMMENT_CHAR + WC_MARK[0] + BC_MARK[0]

    wcList = [] # WhiteCards
    bcList = [] # BlackCards

    reading_bc = False

    try:
        file = open(filepath,"r")
    except IOError:
        print("Error: Couldn't open and read file")
        exit(1)

    for line in file:

        line = line.strip(" \n")
        if not line: continue

        if line[0] in IGNORE_CHARS:
            if   BC_MARK in line: reading_bc = True
            elif WC_MARK in line: reading_bc = False
            continue

        if reading_bc: bcList.append(line)
        else:          wcList.append(line)

    file.close()

    # Unifying "_" on Black Cards: "____" --> "_"
    unifyOnList(bcList, BC_BLANK_CHAR)

    return (wcList, bcList)