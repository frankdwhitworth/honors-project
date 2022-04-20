#!/usr/bin/python3
#
#
# massive_experiment.py  v0.1  Dixon  2.14.2022
#
# runs experiments for my honors thesis and collects 
# the results AND also analyzes/collates them (pretty cool, huh)
# if more instruction needed, see https://www.youtube.com/watch?v=EGeoG0KQa68
#
# Usage
#  just call it, brah 
# 
#  Result:
#   - Main results in tabular format are displayed in command line
#   - A .pkl file is written that has the results dictionary loaded
#   * Working on outputing a .tex file for easy translation lol
#
# Examples
#  Just run it lol
#     python3 ./massive_experiment.py
#   
#  Actually..... I like running this: 
#       
#       nohup ./massive_experiment.py > output.txt 2> output.err &


import sys
import os
import subprocess
import re
import json
import pickle
from datetime import datetime
import math
import shutil

def main(argv):
    time_1 = subprocess.run(['date', '+%s%N'], stdout=subprocess.PIPE)
    time1=time_1.stdout
    address="/home/whitfd18/Knarf/"
    os.system('rm /home/whitfd18/Knarf/Results/*')

    # date = datetime.now().strftime("%I:%M--%m_%d_%Y")
    date = datetime.now().strftime("%m_%d_%Y--%I:%M")
    results_file_name = "/home/whitfd18/Knarf/Full_Results/" + date + "__tabular-results.res"

    # initializing variables
    four_choice_set = 0 # Keeps track of which Xfour_choice.c we are on
    sub_exp = 0         # Keeps track of 
    inputs = 8          # Startin num of inputs for experiments
    experiments=['lib0', 'lib3', 'no_lib0', 'no_lib3'] # list of experiment code names
    exper_count=0       # Keeps track of experiment count for analytics
    run_time_count=0    # Keeps track of finding average ARI for each exper
    # avg_per_num = 100   # Finding average ARI per x experiments
    # for testing
    # avg_per_num = 1     # this is when i just want one run per exper
    avg_per_num = 10
    count_exper_prob = 0
    input_max=4
    four_choice_count=11     # give me the file COUNT 
    #                       if there is a 9four_choice.c, then = 10
    p = 0                   # keeping up with making the res dict
    tot_expers = 288 * len(experiments) * four_choice_count * avg_per_num 
    # 288 above is from adding up the inputs for each sub-experiment

    # important experiment parameters
    c_program_base_path = "/home/whitfd18/Knarf/code_files/four_programs/"

    # setting up our results dictionary
    #   see table in Outline google doc if clarification
    #   is needed (example: results['libraries'][0] then holds a list of 100 results)
    
    # results={ 0: {}, 1: {}, 2: {}, 3: {}, 4: {}, 5: {}}
    # print(results)
    results={}
    while p < four_choice_count:
        results[p]={}
        p+=1
    # print(results)
    temp=0
    for elem in results:
        # print(results[elem])
        for exper in experiments:
            results[elem][exper]={}     # this will have a dict for each set 
            #                               of inputs (0=8, 1=16, 2=32, etc.)
            # while temp<6:     # 8-256 inputs
            while temp<input_max:       # 8-64 inputs
                count_exper_prob+=1
                results[elem][exper][temp] = [] # this list will have the ARIs 
                #                                   from each experiment
                # results[elem][exper][temp].append(0)
                temp+=1
            temp=0
    averages = results
    # printProgressBar(exper_count, tot_expers)
    # while four_choice_set < 4:
    for elem in results:
        c_program_path = c_program_base_path + str(four_choice_set) + "four_choice.c"
        exper_command = "./run_exper.sh " + c_program_path
        # print("- - Four Choice #" + str(four_choice_set) + " [" + c_program_path + "] - - ")
        for exper in experiments:
            # Running overall exper
            # while sub_exp < 6:  # tracking inputs (8, 16, 32, 64, 128, and 256)
            for rez_list in results[elem][exper]: 
                # run sub_exper 100 times
                # input_command = "python3 ./making_args.py " + str(inputs)
                input_exec_path = ["/home/whitfd18/Knarf/code_files/making_args.py", str(inputs)]
                proc = subprocess.Popen(input_exec_path, stdout=subprocess.PIPE)
                (out, err) = proc.communicate()

                # print(exper + " #" + str(sub_exp) + " (" + str(inputs) + " inputs)")

                ari_sum = 0
                sil_sum = 0
                ari_avg = 0
                sil_avg = 0

                while run_time_count < avg_per_num:     # running 10 expers per input #
                    # run the experiment here

                    ari_path = "/home/whitfd18/Knarf/Results/"
                    exper_cmd = ["./run_exper.sh"]
                    exper_cmd.append(c_program_path)
                    if exper == "lib0":
                        # exper_cmd.append("-O0")
                        exper_cmd.append("-O0")
                        exper_cmd.append("-l")
                        ari_path += str(four_choice_set) + "four_choice-LIB-O0-" + str(inputs) + ".res"
                    elif exper == "lib3":
                        exper_cmd.append("-O3")
                        exper_cmd.append("-l")
                        ari_path += str(four_choice_set) + "four_choice-LIB-O3-" + str(inputs) + ".res"
                    elif exper == "no_lib0":
                        # exper_cmd.append("-O0")
                        exper_cmd.append("-O0")
                        exper_cmd.append("no_lib")
                        ari_path += str(four_choice_set) + "four_choice-NOLIB-O0-" + str(inputs) + ".res"
                    elif exper == "no_lib3":
                        exper_cmd.append("-O3")
                        exper_cmd.append("no_lib")
                        ari_path += str(four_choice_set) + "four_choice-NOLIB-O3-" + str(inputs) + ".res"
                    exper_cmd.append(str(inputs))
                    
                    # Example exper_cmd:
                    #  ["./run_exper.sh", c_program_path, "-O0", "-l", inputs, str(elem)]
                    
                    exper_cmd.append(str(elem))

                    # print(exper_cmd)
                    #printing details
                    print(". . .")
                    print("Four Choice: " + str(four_choice_set))
                    print("Experiment: " + exper)
                    print("Inputs: " + str(inputs))
                    print("Local Exper #: " + str(run_time_count))
                    
                    delim_pattern = '6969;(.*);6969'
                    sil_pattern = '420;(.*);420'
                    proc = subprocess.Popen(exper_cmd, stdout=subprocess.PIPE)
                    (out, err) = proc.communicate()
                    ari_num=0
                    """   # Doesn't work now because of ./Results/* output now 
                    if (re.search(delim_pattern, str(out))):
                        ari_num=re.search(delim_pattern, str(out)).group(1)
                    """
                    
                    out_file = open(ari_path, "r")
                    out_str = out_file.read()
                    out_file.close()
                    if (re.search(delim_pattern, out_str)):
                        ari_num=re.search(delim_pattern, out_str).group(1)
                    if (re.search(sil_pattern, out_str)):
                        sil_num=re.search(sil_pattern, out_str).group(1)
                    
                    # print(ari_num)
                    # print(sil_num)

                    if float(ari_num) <= 0:
                        ari_sum+=0
                    else: 
                        ari_sum+=float(ari_num)
                    
                    if float(sil_num) <= 0:
                        sil_sum+=0
                    else:
                        sil_sum+=float(sil_num)

                    # print("ARI Sum = " + str(ari_sum))
                    # print("SIL Sum = " + str(sil_sum))
                    # print("Run Count = " + str(run_time_count+1))

                    # if (run_time_count != 0):
                        # print("-Running Averages-")
                        # print("ARI Average = " + str(float(ari_sum/(run_time_count+1))))
                        # print("SIL Average = " + str(float(sil_sum/(run_time_count+1))))
                        # print("")

                    # save ari bitch
                    # results[elem][exper][rez_list].append(1)
                    if (avg_per_num == 1):
                        results[elem][exper][rez_list].append(ari_num)
                        results[elem][exper][rez_list].append(sil_num)
                    # analytics
                    exper_count+=inputs
                    run_time_count+=1
                    # printProgressBar(exper_count, tot_expers)
                    print(str(exper_count) + " / " + str(tot_expers))
                # variable updates
                ari_avg = ari_sum/avg_per_num
                sil_avg = sil_sum/avg_per_num
                results[elem][exper][rez_list].append(ari_avg)
                results[elem][exper][rez_list].append(sil_avg)

                inputs*=2
                # inputs+=8
                sub_exp+=1
                run_time_count=0
            inputs=8
            sub_exp=0
        four_choice_set+=1
    
    
    time_2 = subprocess.run(['date', '+%s%N'], stdout=subprocess.PIPE)
    time2=time_2.stdout

    t1=str(time1).replace("b\'","")
    t1=int(t1.replace("\\n\'",""))
    t2=str(time2).replace("b\'","")
    t2=int(t2.replace("\\n\'",""))
    print(t1, t2)
    tot_time=t2-t1
    print("Total time: (nanoseconds) " + str(tot_time))
    tot_sec=tot_time / 1e9
    m, s = divmod(tot_sec, 60)
    h, m = divmod(m, 60)

    print("Total time: (seconds)     " + str(tot_sec))
    print("Total time: (minutes)     " + str(m))
    print("Total time: (hours)       " + str(h))

    
    print(results)
    print("\n. . . . . . .")
    print(". Analytics .")
    print(". . . . . . .")
    print("Experiments Ran: \t" + str(exper_count))
    # print("Inputs Processed: \t" + str(input_count))
    
    with open('exper_results.pkl', 'wb') as picklerick:
        pickle.dump(results, picklerick, protocol=pickle.HIGHEST_PROTOCOL)
    
    # We are writing our table to results_file_name (see above)
    f = open(results_file_name, "w")
    y = 0
    print("\nARI Scores: ")
    for elem in results:
        print("\n\nFour_Choice #" + str(elem))
        print("\n{:<12} {:<12} {:<12} {:<12} {:<12} {:<12} {:<12} {:<12} {:<12}".format("FLAGS", "8 INPUTS", "16 INPUTS", "24 INPUTS", "32 INPUTS", "40 INPUTS", "48 INPUTS", "52 INPUTS", "64 INPUTS"))
        print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")
        for exper in experiments:
            table_row="{:<12}".format(exper)
            for rez_list in results[elem][exper]:
                table_row+=" {:<12}".format(truncate(results[elem][exper][rez_list][0], 7))
            print(table_row)

    print("\n\n\n\nSil Scores: \n")
    for elem in results:
        print("\n\nFour_Choice #" + str(elem))
        print("\n{:<12} {:<12} {:<12} {:<12} {:<12} {:<12} {:<12} {:<12} {:<12}".format("FLAGS", "8 INPUTS", "16 INPUTS", "24 INPUTS", "32 INPUTS", "40 INPUTS", "48 INPUTS", "52 INPUTS", "64 INPUTS"))
        f.write("\n")
        print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")
        for exper in experiments:
            table_row="{:<12}".format(exper)
            for rez_list in results[elem][exper]:
                table_row+=" {:<12}".format(truncate(results[elem][exper][rez_list][1], 7))
            print(table_row) 
    

    f.write("\n. . . . . . .\n")
    f.write(". Analytics .\n")
    f.write(". . . . . . .\n")

    f.write("\nExpers Ran for Average: " + str(avg_per_num) + "\n")
    f.write("# of four_choice.c: " + str(four_choice_count) + "\n")
    f.write("\nExperiment Run-Time: " + str(tot_sec) + " seconds\n")
    f.write("Run-Time: " + str(tot_sec) + " seconds\n")
    f.write("Run-Time: " + str(m) + " minutes\n")
    f.write("Run-Time: " + str(h) + " hours\n")

    f.write("\nARI Scores: ")
    f.write("\n")
    for elem in results:
        f.write("\n\nFour_Choice #" + str(elem))
        f.write("\n")
        f.write("\n{:<12} {:<12} {:<12} {:<12} {:<12} {:<12} {:<12} {:<12} {:<12}".format("FLAGS", "8 INPUTS", "16 INPUTS", "24 INPUTS", "32 INPUTS", "40 INPUTS", "48 INPUTS", "52 INPUTS", "64 INPUTS"))
        f.write("\n")
        f.write("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")
        f.write("\n")
        for exper in experiments:
            table_row="{:<12}".format(exper)
            for rez_list in results[elem][exper]:
                table_row+=" {:<12}".format(truncate(results[elem][exper][rez_list][0], 7))
            f.write(table_row)
            f.write("\n")       

    f.write("\n\n\n\nSil Scores: \n")
    f.write("\n")
    for elem in results:
        f.write("\n\nFour_Choice #" + str(elem))
        f.write("\n")
        f.write("\n{:<12} {:<12} {:<12} {:<12} {:<12} {:<12} {:<12} {:<12} {:<12}".format("FLAGS", "8 INPUTS", "16 INPUTS", "24 INPUTS", "32 INPUTS", "40 INPUTS", "48 INPUTS", "52 INPUTS", "64 INPUTS"))
        f.write("\n")
        f.write("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")
        f.write("\n")
        for exper in experiments:
            table_row="{:<12}".format(exper)
            for rez_list in results[elem][exper]:
                table_row+=" {:<12}".format(truncate(results[elem][exper][rez_list][1], 7))
            f.write(table_row) 
            f.write("\n")   
    
    f.close()   

    print("Done!")

        


# eh, will implement later... 
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    prefix="Progress:"
    suffix="Complete"
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    styling = '%s |%s| %s%% %s' % (prefix, fill, percent, suffix)
    cols, _ = shutil.get_terminal_size(fallback = (length, 1))
    length = cols - len(styling)
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    
    # Print New Line on Complete
    if iteration == total: 
        print()
    

def truncate(number, decimals=0):
    """
    Returns a value truncated to a specific number of decimal places.
    """
    if not isinstance(decimals, int):
        raise TypeError("decimal places must be an integer.")
    elif decimals < 0:
        raise ValueError("decimal places has to be 0 or more.")
    elif decimals == 0:
        return math.trunc(number)

    factor = 10.0 ** decimals
    return math.trunc(number * factor) / factor


    
if __name__=="__main__":
    main(sys.argv)
