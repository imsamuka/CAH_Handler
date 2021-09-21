# Constants
WC_MARK = "[WHITECARDS]"
BC_MARK = "[BLACKCARDS]"
BC_BLANK_CHAR = "_"
COMMENT_CHAR = "#"

# Functions

def unifyOnList(strings, char):
    dchar = char+char
    for i in range(len(strings)):
        while dchar in strings[i]:
            strings[i] = strings[i].replace(dchar,char)

def repeatOnList(strings, char, n):
    nchar = char*n
    for i in range(len(strings)):
        if char in strings[i]:
            strings[i] = strings[i].replace(char,nchar)

def readTxtFile(filepath):
    wcList = [] # WhiteCards
    bcList = [] # BlackCards

    file = open(filepath,"r")

    readingBlackCards = False
    line = file.readline()
    while line:

        line = line.strip(" \n")

        if not line:
            line = file.readline()
            continue

        if WC_MARK[0] == line[0] or BC_MARK[0] == line[0]  or COMMENT_CHAR == line[0]:
            if BC_MARK in line:
                readingBlackCards = True
            elif WC_MARK in line:
                readingBlackCards = False
            line = file.readline()
            continue

        if readingBlackCards:
            bcList.append(line)
        else:
            wcList.append(line)
        line = file.readline()

    # Unifying "_" on Black Cards: "____" --> "_"
    unifyOnList(bcList,BC_BLANK_CHAR)

    return wcList, bcList