
1/21/2022

Frank Edit: 1/21/2022 @ 1358
* I added /Knarf/Outputs to be the destination of all the output files (ins, prf, out)

this tool chain will run a program that expects different command arguments
then attempts to cluster the resulting instruction profiles, hopefully executions
that used arguments that invoked the same set of code will cluster together

currently simple.c will take one argument, if the argument is an int it does a
summation, if the argument is an alphabet-string then it will count the number of 'a'
(so simple.c does 2 different things based on the argument provided)

steps for a complete experiment:

1. edit and compile simple.c (executable is called a.out)

2. create a file called "command_args.txt" each line of this file will be an execution
where the line consists of the command line argument to use

3. run papa.py, will read commands_args.txt and run a.out using the command line arguments provided
in command_args.txt, so if commands_args.txt has 10 lines then there will be 10 executions of a.out
to run papa.put do the following

  ./papa.py -c "./a.out" -a command_args.txt

3A. after papa.py has executed your directory will have *.prf *.ins and *.out files that contain
   *.prf contains the instruction profiles
   *.int contains the instructions executed
   *.out contains the output to the screen

   so there are 3 files created by papa.py per a.out execution (10 lines in command_args.txt means 30 files created)

   note the file names, if the execution was "./a.out aaa" (done by papa.py) then the resulting files are
     a.out_aaa_no_lib_19.ins
     a.out_aaa_no_lib_19.prf
     a.out_aaa_no_lib_19.out

     the "no_lib" means no library calls were included (option for papa.py, default is no library calls)
     and the number "19" (in this case) is just the line number from command_args.txt or the 19th run
     executed (not useful at the moment)

** to use an instruction map, add the "-m" flag and mapping file to papa.py

  ./papa.py -c "./a.out" -a command_args.txt -m intel4.map

note, intel20.map maps all instructions into one of 4 catgories (instructions),
intel4.map maps all instruction to one of 4 instructions 


**** (Frank Edit)
3B. I added an output directory for the ins, prf, and out files

4. cluster with gmm_cluster.py for example the following will cluster using all the *.prf files in the current directory

  python3 gmm_cluster.py -r ./Outputs/*.prf


* * * * * * * *
New script to run! 

This script will run the entire experiment for you:
  
  ./run_exper.sh simple.c command_args.txt
