import pickle
import math
import sys

def main(argv):
    experiments=['lib0', 'lib3', 'no_lib0', 'no_lib3'] # list of experiment code names

    file = open('exper_results.pkl', 'rb')
    results = pickle.load(file)
    file.close()

    print("\n. . . . . . .")
    print(". Analytics .")
    print(". . . . . . .")

    # We are writing our table to results_file_name (see above)
    f = open('shit_testing.txt', "w")

    print("\nARI Scores: ")
    for elem in results:
        print("\n\nFour_Choice #" + str(elem))
        print("\n{:<12} {:<12} {:<12} {:<12} {:<12}".format("FLAGS", "8 INPUTS", "16 INPUTS", "32 INPUTS", "64 INPUTS"))
        print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")
        for exper in experiments:
            table_row="{:<12}".format(exper)
            for rez_list in results[elem][exper]:
                table_row+=" {:<12}".format(truncate(results[elem][exper][rez_list][0], 7))
            print(table_row)

    print("\n\n\n\nSil Scores: \n")
    for elem in results:
        print("\n\nFour_Choice #" + str(elem))
        print("\n{:<12} {:<12} {:<12} {:<12} {:<12}".format("FLAGS", "8 INPUTS", "16 INPUTS", "32 INPUTS", "64 INPUTS"))
        f.write("\n")
        print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")
        for exper in experiments:
            table_row="{:<12}".format(exper)
            for rez_list in results[elem][exper]:
                table_row+=" {:<12}".format(truncate(results[elem][exper][rez_list][1], 7))
            print(table_row) 
    

    f.write("\n. . . . . . .\n")
    f.write(". Analytics .\n")
    f.write(". . . . . . .\n")

    f.write("\nARI Scores: ")
    f.write("\n")
    for elem in results:
        f.write("\n\nFour_Choice #" + str(elem))
        f.write("\n")
        f.write("\n{:<12} {:<12} {:<12} {:<12} {:<12}".format("FLAGS", "8 INPUTS", "16 INPUTS", "32 INPUTS", "64 INPUTS"))
        f.write("\n")
        f.write("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")
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
        f.write("\n{:<12} {:<12} {:<12} {:<12} {:<12}".format("FLAGS", "8 INPUTS", "16 INPUTS", "32 INPUTS", "64 INPUTS"))
        f.write("\n")
        f.write("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")
        f.write("\n")
        for exper in experiments:
            table_row="{:<12}".format(exper)
            for rez_list in results[elem][exper]:
                table_row+=" {:<12}".format(truncate(results[elem][exper][rez_list][1], 7))
            f.write(table_row) 
            f.write("\n")   
    f.close()   

    print("All done")


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
