#!/usr/bin/python3

#
# pappy.sh  v0.8  E.W.Fulp  3/29/2019
#
# run snooper3 in parallel, also provides mapping and removal of library
# instructions if requested (command line arguments), thus it requires
# mappy.py as well (see https://www.youtube.com/watch?v=EGeoG0KQa68)
#
# Usage
#  papa.py [-l] [-m <map_file>] [-s <number>] -c "command_and_flags" -a "argument_file"
#   -l  include libraries
#   -m <map_file>  map instructions using map_file
#   -s <number> the first percentage of intructions to sample (ex. 20)
#   -e <number>   number of instructions to process (from the beginning, applied AFTER no-lib)
#   -c "command_and_flags"  command with flags to execute (REQUIRED)
#   -a "argument_file"  list of arguments to pass to the command (REQUIRED)
#
#  Result:
#   *.ins file of the instructions (after -l and/or -e options applied)
#   *.prf instruction profile (based on *.ins)
#   *.mins if mapping, mapped instruction file (based on *.ins)
#   *.mprf if mapping, mapped instruction profile (based on *.ins)
#   *.out file containing the command output (stdout only)
#
#  FIXES:
#   (3/2/2019) removed '\n' from the end of every argument line from argument_file,
#    this was causing errors with certain commands (gzip and wget)
#   (3/29/2019) changed snooper3 command to use "-f" option so snooper3 saves the
#    instructions directly into the file (does not rely on ">" redirect)
#
#  ACHTUNG! the "" around the command_and_flags is required to preserve
#  spaces in the command, for example "ls -al"
#
#  -e <number> is applied after removing the library calls (which should make sense...)
#
#  argument_file is a file containing arguments for each run (one line per
#  experiment). So, if you want to run "ls -al" three times, each with a
#  different directory, the file contents would look like
#   /home/whitenpm
#   /home/rick
#   /home/roll
#
# creates the following files (note, will depend on pappy.py arguments)
#  command_and_flags_argument_some_number.ins  Intel instructions executed
#  command_and_flags_argument_some_number.prf  profile of Intel instructions
#  command_and_flags_argument_some_number.mins mapped Intel instr executed
#  command_and_flags_argument_some_number.prf  profile of mapped Intel instr
#
# Examples
#  Run pappy.py for experiments with ls -al use argument file lsFiles.txt
#  include libraries but no mapping
#   ./pappy -l -c "ls -al" -a ./lsFiles.txt
#
#  same experiment but do mapping with the file intel.map
#   ./pappy.py -l -c "ls -al" -a ./lsFiles.txt -m intel.map
#

import subprocess
import sys
import getopt
import os.path
import copy
import mapa
#import samply
#import constant
from subprocess import Popen, PIPE, STDOUT
try:
    from subprocess import DEVNULL
except ImportError:
    import os
    DEVNULL = open(os.devnull, 'wb')
# you need to set the following depending on the experiment


def help(prog_name):
    print('useage: ' + prog_name + ' [-l] [-m <map_file>] [-s <number>] -c "command_and_flags" -a argument_file ')
    print('-l  include libraries ')
    print('-e <number>  number of instructions to process (from the beginning, applied after -l) ')
    print('-s <number> the pecentage of instructions to process (from the beginning)')
    print('-m <map_file>  map instructions using map_file ')
    print('-c "command_and_flags"  command with flags to execute (REQUIRED) ')
    print('-a argument_file  file with arguments to pass to command (REQUIRED) ')


def main(argv):
    prog_name = os.path.basename(__file__)
    out_file_names = []
    pid_count = {}
    cmd_processes = []
    prf_processes = []
    count = 0

    # let's make certain snopper2 is about
    if not os.path.isfile("./snooper3"):
        print(prog_name + ' requires snooper3 to reside in the same directory')
        print("I couldn't find it... better luck next time Arnav ")
        sys.exit(2)

    # get command line arguments
    cmd = ''
    cmd_arg_file = ''
    inc_libraries = 'no_lib'
    map_file = ''
    max_num_instr = -1
    sample_percent = -1
    try:
        opts, args = getopt.getopt(argv,"hlc:a:m:e:s:",["command=","args=", "map="])
    except getopt.GetoptError:
        help(prog_name)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            help(prog_name)
            sys.exit()
        elif opt in ("-c", "--command"):
            cmd = arg
        elif opt in ("-a", "--args"):
            cmd_arg_file = arg
        elif opt in ("-e", "--end"):
            try:
                max_num_instr = int(arg)
            except ValueError:
                help(prog_name)
                system.exit()
        elif opt in ("-s", "--sample"):
            try:
                sample_percent = int(arg)
            except ValueError:
                help(prog_name)
                system.exit()
        elif opt in ("-m", "--map"):
            # let's make certain the map file is about
            if not os.path.isfile("./mapa.py"):
                print(prog_name + ' requires mapa.py to reside in the same directory')
                print("I couldn't finu it... better luck next time Arnav ")
                sys.exit(2)
            map_file = arg
            if not os.path.isfile(map_file):
                print(prog_name + " couldn't find map_file " + map_file)
                sys.exit(2)
        elif opt == '-l':
            inc_libraries = 'inc_lib'

    if not cmd or not cmd_arg_file:
        help(prog_name)
        sys.exit(2)
    output_dir = "/home/whitfd18/Knarf/Outputs/"
    with open(cmd_arg_file) as open_file_object:
        for line in open_file_object:
            # FIX: (3/2/2019) remove the carrage return found at the end of every line... sigh...
            line = line.replace('\n', '')
            limit_instr = ''
            if max_num_instr != -1:
                limit_instr = "_e" + str(max_num_instr)
            out_file = output_dir + (cmd.replace(' ', '_')).replace('-', 'D') + '_' + ((line.replace(' ', '_')).replace('/', '.')).replace('\n', '') + '_' + inc_libraries + limit_instr + '_' + str(count) + '.ins'
            # out_file_names.append(out_file)

            # NEW: (3/29/2019) have snooper3 save instructions using "-f" option
            # otherwise command output is mingled with the instruction file...
            command =  './snooper3 -f ' + out_file + ' ' + cmd + ' "' + str(line)  + '" '
            # urint "1. command", command
            # add command for no libraries
            if inc_libraries == 'no_lib':
                # command += '&& grep "^00005" ' + out_file + ' '
                command += '-a 00005 '
            # print "2. command", command
            # add command for max line limit
            if max_num_instr != -1:
                # command += '| ' + "awk 'NR <= " + str(max_num_instr) + " {print $0;}' "
                command += '-n ' + str(max_num_instr)
            # print "3. command", command
            out_file_names.append(out_file)
            out_file = out_file.replace('.ins', '.out')
            command += '> ' + out_file + ' 2>&1 '
            # print "4. command", command
            # print('COMMAND: ', command)
            # out_file_names.append(out_file)
            p = subprocess.Popen(command, stdout = DEVNULL, stderr = STDOUT, shell = True)
            # p = subprocess.Popen('./snooper3 -f ' + out_file + ' ' + cmd + ' ' + str(line), stdout = DEVNULL, stderr = STDOUT, shell = True)
            cmd_processes.append(p)  # start one, and immediately start another
            pid_count.update({p: count})  # dict of process id and count
            count = count + 1
    open_file_object.close()

    print(prog_name + ': running ' + str(count) + ' snooper3 experiments')

    # join command processes together, start another process for profile gen
    for cp in cmd_processes:
        print('lets wait')
        cp.wait()
        # print 'cp', cp, 'pid_count', pid_count[cp]
        suffix = '.ins'
        # if max_num_instr != -1:
        #     suffix = '.out'
        print('finished waiting')
        run_file = out_file_names[pid_count[cp]]
        map_run_file = run_file.replace(suffix, ".mins")
        sample_run_file = run_file.replace(suffix, ".sins")
        prof_file = run_file.replace(suffix, ".prf")
        # This is to output in the ./Output/ directory
        prof_file = prof_file.replace("./", "")
        map_prof_file = run_file.replace(suffix, ".mprf")
        print(prog_name + ': processing ' + run_file + ' to produce profiles')

        # you've asked for only the first max_num_instr to be considered
        # build the command string to process the instruction file

        # following should be done in Python...
        # command = map_cmd + lib_cmd +  "awk '{print $3}'" + ' | tr \"\" \"\n\"| sort | uniq -c > ' + prof_file

        # open the instruction file for reading

        file_to_use = run_file

        # print('RUN FILE: ', file_to_use)
        # once we have the instructions, we want to sample the first x% of instructions
        if sample_percent != -1:
            samply.sample(run_file, sample_run_file, sample_percent, constant.RAND)
            file_to_use = sample_run_file


        print('MAP RUN FILE: ', map_run_file)
        if map_file:
            mapa.map(map_file, file_to_use, map_run_file, max_num_instr)
            file_to_use = map_run_file

        opcodes_dict = {}

        print('USING INSTRUCTION FILE: ', file_to_use)

        with open(file_to_use, encoding='ascii') as f:
            for line in f:
                if line.split()[1] == 'c4' or line.split()[1] == 'c5':
                    continue
                op_code = line.split()[2]
                if op_code in opcodes_dict:
                    opcodes_dict[op_code] += 1
                else:
                    opcodes_dict[op_code] = 1

        # open profile file for writing
        # temp_file_name = output_dir + prof_file
        print('PROFILE; ', prof_file)
        with open(prof_file, "w+") as f:
            for i in sorted(opcodes_dict):
                f.write("{:>7} {:7}\n".format(opcodes_dict[i], i))

        opcodes_dict.clear()

        # print command
        # command = 'cat ' + run_file + " | awk '{print $3}'" + ' | tr \"\" \"\n\"| sort | uniq -c > ' + prof_file
        # command = './mappy.py -m intel.map -i ' + run_file + " | awk '{print $3}'" + ' | tr \"\" \"\n\"| sort | uniq -c > ' + prof_file
        # command = './mappy.py -m intel.map -i ' + run_file + ' > ' + map_file + ' && cat ' + map_file + ' | grep "^00000000004"'  + " | awk '{print $3}'" + ' | tr \"\" \"\n\"| sort | uniq -c > ' + prof_file

    print('fin ')


if __name__ == "__main__":
   main(sys.argv[1:])
