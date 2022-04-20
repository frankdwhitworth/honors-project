#!/bin/bash
# This will run the papa experiment with the 
#    given c file. It will compile the c file,
#    run the experiments, and run the clustering
#    as well. 
#  Usage:
#  ["./run_exper.sh", c_program_path, "-O0", "-l", inputs]		    
#
#                   c file   commands file

# Making sure we are in the right place...
cd /home/whitfd18/Knarf

# removes all output files to setup for experiment
rm /home/whitfd18/Knarf/Outputs/*

echo $0
echo $1
echo $2
echo $3
echo $4
echo $5 

# Here is the c file we are testing - notice the optomization 
# gcc $1 -O0 -lm
gcc $1 $2 -lm

# ./papa.py -c "./a.out" -a $2 -m intel20.map

COMP_STR="-l"

if [ "$COMP_STR" = "$3" ];
  then
    #echo found lib param
    # ./papa.py -c "./a.out" -a code_files/command_args_four_choice.txt
    # FILENAME="${1:46:12}-LIB$2-$4.res"
    FILENAME="$5four_choice-LIB$2-$4.res"
    echo $FILENAME 
    ./papa.py -c "./a.out" -l -a code_files/command_args_four_choice.txt
  else
    # echo didn't find lib param
    # ./papa.py -c "./a.out" -l -a code_files/command_args_four_choice.txt
    # FILENAME="${1:46:12}-NOLIB$2-$4.res"
    FILENAME="$5four_choice-NOLIB$2-$4.res"
    echo $FILENAME
    ./papa.py -c "./a.out" -a code_files/command_args_four_choice.txt
fi

python3 gmm_cluster.py -r ./Outputs/*.prf > /home/whitfd18/Knarf/Results/$FILENAME

echo 
echo . . . 
echo 
echo done boi
