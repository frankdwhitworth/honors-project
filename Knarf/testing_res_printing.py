# plz run from inside ./Knarf directory

import sys
import os
import subprocess
import re
import json
import pickle
import math

def main(argv):
    time_1 = subprocess.run(['date', '+%s%N'], stdout=subprocess.PIPE)
    time1=time_1.stdout
    picklerick = open('exper_results.pkl', 'rb')
    results = pickle.load(picklerick)
    picklerick.close()
    experiments=['lib0', 'lib3', 'no_lib0', 'no_lib3']
    for elem in results:
        print("\n\nFour_Choice #" + str(elem))
        print("\n{:<12} {:<12} {:<12} {:<12} {:<12}".format("FLAGS", "8 INPUTS", "16 INPUTS", "32 INPUTS", "64 INPUTS"))
        print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")
        for exper in experiments:
            table_row="{:<12}".format(exper)
            for rez_list in results[elem][exper]:
                table_row+=" {:<12}".format(truncate(results[elem][exper][rez_list][0], 7))
            print(table_row)       
        # print(results[elem])
    
    print("\n\nSil. Time :3\n")
    for elem in results:
        print("\n\nFour_Choice #" + str(elem))
        print("\n{:<12} {:<12} {:<12} {:<12} {:<12}".format("FLAGS", "8 INPUTS", "16 INPUTS", "32 INPUTS", "64 INPUTS"))
        print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")
        for exper in experiments:
            table_row="{:<12}".format(exper)
            for rez_list in results[elem][exper]:
                table_row+=" {:<12}".format(truncate(results[elem][exper][rez_list][1], 7))
            print(table_row)       
        # print(results[elem])

    tex_strs=[]
    
    for elem in results:
        temp_str="""\\begin{table}[ht]
\\centering % used for centering table
\\resizebox{\\textwidth}{!}{
\\begin{tabular}{c c c c c} % centered columns (4 columns)
% \\hline
Sub-Experiment Flags & 8 Inputs ARI & 16 Inputs ARI & 32 Inputs ARI & 64 Inputs ARI \\\\ [0.5ex] % inserts table
%heading
\\hline\\hline %inserts double horizontal lines
"""
        for exper in experiments:
            if exper == 'lib0':
                temp_str += "\\verb|-O0 -lib|"
            elif exper == 'lib3':
                temp_str += "\\verb|-O3 -lib|"
            elif exper == 'no_lib0':
                temp_str += "\\verb|-O0 -nolib|"
            elif exper == 'no_lib3':
                temp_str += "\\verb|-O3 - nolib|"

            for rez_list in results[elem][exper]:
                temp_str += " & "
                temp_str += str(truncate(results[elem][exper][rez_list][0], 7))
            temp_str += " \\\\\n\\hline\n"
        temp_str += """\end{tabular}}
\caption{Four Choice """ + str(elem) + """ Clustering ARI Scores} % title of Table
\label{fc0} % is used to refer this table in the text
\end{table}"""   
        print(temp_str)
        print()
        # print(results[elem])


    print("\n\nSil. Time :3\n")
    for elem in results:
        print(str(elem))
        temp_str="""\\begin{table}[ht]
\\centering % used for centering table
\\resizebox{\\textwidth}{!}{
\\begin{tabular}{c c c c c} % centered columns (4 columns)
% \\hline
Sub-Experiment Flags & 8 Inputs S.S. & 16 Inputs S.S. & 32 Inputs S.S. & 64 Inputs S.S. \\\\ [0.5ex] % inserts table
%heading
\\hline\\hline %inserts double horizontal lines
"""
        for exper in experiments:
            if exper == 'lib0':
                temp_str += "\\verb|-O0 -lib|"
            elif exper == 'lib3':
                temp_str += "\\verb|-O3 -lib|"
            elif exper == 'no_lib0':
                temp_str += "\\verb|-O0 -nolib|"
            elif exper == 'no_lib3':
                temp_str += "\\verb|-O3 - nolib|"

            for rez_list in results[elem][exper]:
                temp_str += " & "
                temp_str += str(truncate(results[elem][exper][rez_list][1], 7))
            temp_str += " \\\\\n\\hline\n"
        temp_str += """\end{tabular}}
\caption{Four Choice """ + str(elem) + """ Clustering Silhouette Scores} % title of Table
\label{fc0} % is used to refer this table in the text
\end{table}"""   
        print(temp_str)
        print()
    
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
    # tot_sec=120000  # this is just for testing
    m, s = divmod(tot_sec, 60)
    h, m = divmod(m, 60)

    print("Total time: (seconds)     " + str(tot_sec))
    print("Total time: (minutes)     " + str(m))
    print("Total time: (hours)       " + str(h))


def truncate(number, decimals=0):
    if not isinstance(decimals, int):
        raise TypeError("decimal place must be an int")
    elif decimals < 0:
        raise ValueError("decimal place has to be 0 or more")
    elif decimals == 0:
        return math.trunc(number)

    factor = 10.0 ** decimals
    return math.trunc(number * factor) / factor
        
    
if __name__=="__main__":
    main(sys.argv)
