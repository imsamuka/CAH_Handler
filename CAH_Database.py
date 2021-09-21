# Default Characters
wcIdentifier = "[WHITECARDS]"
bcIdentifier = "[BLACKCARDS]"
null_line = "#"
blackCardBlankSpace = "_"
# ----- DataBases -----
# WhiteCards
wcList = []
# BlackCards
bcList = []
# ---------------------

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
    global wcList, bcList
    file = open(filepath,"r")

    readingBlackCards = False
    line = file.readline()
    while line:

        line = line.strip(" \n")

        if not line:
            line = file.readline()
            continue

        if wcIdentifier[0] == line[0] or bcIdentifier[0] == line[0]  or null_line == line[0]:
            if bcIdentifier in line:
                readingBlackCards = True
            elif wcIdentifier in line:
                readingBlackCards = False
            line = file.readline()
            continue

        if readingBlackCards:
            bcList.append(line)
        else:
            wcList.append(line)
        line = file.readline()

    # Unifying "_" on Black Cards: "____" --> "_"
    unifyOnList(bcList,blackCardBlankSpace)

    return wcList, bcList