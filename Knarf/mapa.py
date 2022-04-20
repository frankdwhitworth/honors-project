#!/usr/bin/python3  

#  mappy.py  v0.1 E W Fulp  7/10/2018
#
#  given a snooper output file (list of Intel instructions), this
#  application will map the Intel instructions to a category based
#  on a map file, output is sent to the screen
#
#  useage:
#     ./mappy -i snooperInstructionFile -m mapFile
#
#  ACHTUNG!
#    developed closely with a map file having the following format
#    
#      instruction cat1 cat2 cat3 ...
# 
#    where cat1, cat2, etc.. are categories, for example
#      ADD     gen     arith   binary
#
#    variable cat_index is set to the specific column (hardcoded below)
#
# sanity check via
#   ./mappy.py -i ls.short -m intel.map | awk '{print $3}' | sort | uniq -c
#
# more available at https://www.youtube.com/watch?v=EGeoG0KQa68  

import sys
import getopt  
import copy

def map(map_file, instr_file, out_file, max_num_instr):
    # get command line arguments
    # instr_file = '' 
    # map_file = ''
    # try:
    #     opts, args = getopt.getopt(argv,"hi:m:",["ifile=","mfile="])
    # except getopt.GetoptError:
    #     print 'mappy.py -i <instrfile> -m <mapfile>'
    #     sys.exit(2)
    # for opt, arg in opts:
    #     if opt == '-h':
    #         print 'mappy.py -i <instrfile> -m <mapfile>'
    #         sys.exit()
    #     elif opt in ("-i", "--ifile"):
    #         instr_file = arg
    #     elif opt in ("-m", "--mfile"):
    #         map_file = arg

    # if not map_file is None and not instr_file is None:  
    if not map_file and not instr_file:  
        print('mappy.py -i <instrfile> -m <mapfile>')
        sys.exit(2)

    # print "instr file is ", instr_file
    # print "map file is ", map_file

    # create a map of the instructions to the categories  
    file = open(map_file)
    # the following determines the categories to use (which column in the file)
    cat_index = 2
    instr_map = {} 
    line = (file.readline()).rstrip()
    while line:
        items = (line.split('\t'))  
        # let's make certain the instruction is not already in the map...
        if not items[0] in instr_map:  
            instr_map[items[0]] = items[cat_index].lower()
   
        line = (file.readline()).rstrip()
    file.close()  

    # print instr_map

    # print "number of map entries", len(instr_map)

    res_file = open(out_file, "w")

    file = open(instr_file)
    # the following determines the categories to use (which column in the file)
    cat_index = 1
    line = (file.readline()).rstrip()
    
    count = 0
    while line:
        count = count + 1
        # if max_num_instr != -1:
        #     if count > max_num_instr:
        #         break

        items = (line.split(' '))  
        items = list(filter(None, items))  

        # print items[2], "=>", instr_map[items[2].upper()]
        if not items[2].upper() in instr_map:
            print ("mappy.py: ooops... instruction [", items[2].upper(), "] not in map")
            print ("error when processing:", line)
            sys.exit(2)  
        items[2] = instr_map[items[2].upper()]  
        # output_str = ' '.join(items)
        output_str = items[0] + ' ' + items[1] + '\t' + items[2]
        if len(items) == 4:  
            output_str += ' ' + items[3]  
        elif len(items) == 5 :
            output_str += ' ' + items[3] + ' ' + items[4]
        elif len(items) > 5:  
            output_str += ' ' + items[3]  + ' ' + items[4] + ", "
            output_str += ' '.join(items[5:])
        
        # print output_str
        res_file.write(output_str + '\n')
   
        line = (file.readline()).rstrip()
    res_file.close()
    file.close()  

