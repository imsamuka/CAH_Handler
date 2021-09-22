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

    try: file = open(filepath,"r")
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

def writeTxtFile(
    filepath : str,
    decks : tuple[list[str], list[str]],
    infos : tuple[str, str] = ()
    ) -> None:


    try: file = open(filepath, "w", encoding="utf-8")
    except IOError:
        print("Error: Couldn't open file to write")
        exit(1)

    # Marks
    marks = (WC_MARK, "\n"*4 + BC_MARK)

    # For both decks
    for i in range(2):

        info = ''
        if i < len(infos):
            # Split the info by lines
            info = infos[i].split("\n")

            # Start every line that have something with COMMENT_CHAR
            for k in range(len(info)):
                if info[k]: info[k] = COMMENT_CHAR + info[k]

            # Join the lines together
            info = "\n".join(info)


        # Add the mark
        lines = marks[i] + "\n"

        # Add the info below the mark
        if info: lines += info + "\n"

        # Add '\n' to every line
        lines += "\n".join(decks[i]) + "\n"


        try: file.write(lines)
        except IOError:
            print("Error: Couldn't write to file")
            exit(1)

    file.close()