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

def unifyOnList(List, char):
    i = 0
    doubleChar = char+char
    while i < len(List):
        while doubleChar in List[i]:
            List[i] = List[i].replace(doubleChar,char)
        i += 1
    return

def repeatOnList(List, char, n):
    nTimesChar = char*n
    i = 0
    size = len(List)
    while i < size:
        if char in List[i]:
            List[i].replace(char,nTimesChar)
        i += 1
    return

def clearInString(text,chars = [" ", "\n"]):
    for k in chars:
        for char in chars:
            while text.startswith(char):
                text = text[len(char):]
            while text.endswith(char):
                text = text[:-len(char)]
    return text


def readTxtFile(filepath):
    global wcList, bcList
    file = open(filepath,"r")

    readingBlackCards = False
    line = file.readline()
    while line:

        line = clearInString(line)

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