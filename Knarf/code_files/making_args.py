#!/bin/python3

# making_args.py
#
# Makes arguments to pass to a C file
#  (will dump into one file (command_args_2.txt))

import sys

def main(argv):
    address="/home/whitfd18/Knarf/code_files/command_args_four_choice.txt"
    f = open(address, "w")
    x = 0
    while x < int(argv[1]):
        f.write(str(x) + '\n')
        x+=1
    f.write(str(x))
    x = 0
    # while x < 1034:
    #     f.write(str(x%12) + '\n')
    #     x+=1
    f.close()
    
if __name__=="__main__":
    main(sys.argv)
