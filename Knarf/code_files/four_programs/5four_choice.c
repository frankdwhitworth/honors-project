// This is going to do modular 4 a 
//   given number and do something in result

/* For this one, it is cool because I am also 
testeing to see if optimization also does something...
let's see! */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <math.h>
#include <unistd.h> /* for fork */
#include <sys/types.h> /* for pid_t */
#include <sys/wait.h> /* for wait */

/* our methods for experiments */
#include </home/whitfd18/Knarf/code_files/four.h>

int modFour(int num);

int main(int argc, char *argv[]) {
    int i = 0;
    int res = 0;
    int temp = 4;
    int intValue;
    intValue = atoi(argv[1]);
    temp = modFour(intValue);
    printf("temp=%d\n", temp);
    if (temp==0) {
       	res+=readIt();
        res+=shiftIt(intValue);
        res+=dijkstraIt(temp);
        res+=binaryIt(intValue);
        res+=readIt();
        res+=shiftIt(intValue);
        res+=dijkstraIt(temp);
        res+=binaryIt(intValue);
        res+=readIt();
        res+=readIt();
        res+=readIt();
        res+=readIt();
        res+=readIt();
        res+=readIt();
        res+=shiftIt(intValue);
        res+=dijkstraIt(temp);
        res+=binaryIt(intValue);
        //res+=readIt();
        //res+=shiftIt(intValue);
        //res+=dijkstraIt(temp);
        //res+=binaryIt(intValue);
    } if (temp==1) {
        res+=readIt();
        res+=readIt();
        res+=readIt();
        //res+=readIt();
        res+=shiftIt(intValue);
        res+=shiftIt(intValue);
        res+=shiftIt(intValue);
        res+=shiftIt(intValue);
        res+=shiftIt(intValue);
        res+=shiftIt(intValue);
        res+=shiftIt(intValue);
        //res+=shiftIt(intValue);
        res+=dijkstraIt(temp);
        res+=dijkstraIt(temp);
        res+=dijkstraIt(temp);
        //res+=dijkstraIt(temp);
        res+=binaryIt(intValue);
        res+=binaryIt(intValue);
        res+=binaryIt(intValue);
        //res+=binaryIt(intValue);
    } if (temp==2) {
        res+=binaryIt(intValue);
        res+=dijkstraIt(temp);
        res+=shiftIt(intValue);
       	res+=readIt();
        res+=binaryIt(intValue);
        res+=dijkstraIt(temp);
        res+=dijkstraIt(temp);
        res+=dijkstraIt(temp);
        res+=dijkstraIt(temp);
        res+=dijkstraIt(temp);
        res+=shiftIt(intValue);
       	res+=readIt();
        res+=binaryIt(intValue);
        res+=dijkstraIt(temp);
        res+=shiftIt(intValue);
       	res+=readIt();
        //res+=binaryIt(intValue);
        //res+=dijkstraIt(temp);
        //res+=shiftIt(intValue);
       	//res+=readIt();
    } if (temp==3) {
       	res+=readIt();
        res+=shiftIt(intValue);
        res+=dijkstraIt(temp);
        res+=binaryIt(intValue);
        res+=readIt();
        res+=shiftIt(intValue);
        res+=binaryIt(intValue);
        res+=binaryIt(intValue);
        res+=binaryIt(intValue);
        res+=binaryIt(intValue);
        res+=binaryIt(intValue);    // Switched these
        res+=dijkstraIt(temp);              // two... tehe
        res+=readIt();
        res+=shiftIt(intValue);
        res+=dijkstraIt(temp);
        res+=binaryIt(intValue);
        //res+=readIt();
        //res+=shiftIt(intValue);
        //res+=dijkstraIt(temp);
        //res+=binaryIt(intValue);
    }
    printf("%d\n", res);
    return res;
}


int modFour(int num) {
    return (num%4);
}
