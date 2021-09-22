import CAH_Database
import argparse

def main():

    # ArgumentParser -------------------------------

    parser = argparse.ArgumentParser(description='Rewritte a .txt file of CAH_Database to be a little prettier :D')
    parser.add_argument('--input_file',  type=str, help='the .txt file you want rewritten')
    parser.add_argument('--output_file', type=str, default='', help='the output file. (optional)')
    args = parser.parse_args()

    INPUT_FILE = args.input_file
    OUTPUT_FILE = args.output_file

    # ----------------------------------------------

    fmt = "-formatted"
    winfs = " Each line from here will be considered a WHITE CARD"
    binfs = " Each line from here will be considered a BLACK CARD"

    # ----------------------------------------------

    # If no INPUT_FILE from ArgumentParser, ask in a dialog
    if not INPUT_FILE:
        INPUT_FILE = CAH_Database.dialogSelectInputFile()

    # Still no file? error!
    if not INPUT_FILE:
        print('There is no input file!\n Insert one by adding a "--input_file" argument and then your file')
        exit(1)

    # Use INPUT_FILE + fmt as the default OUTPUT_FILE
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



if __name__ == "__main__":
    main()