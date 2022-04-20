// This is going to do modular 4 a 
//   given number and do something in result

/* Finally doing a baseline test....
I guess? */

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
        for (int i = 0; i < 3; i++)
            res=shiftIt(intValue);
    } if (temp==1) {
        for (int i = 0; i < 10; i++)
            res=shiftIt(intValue);
    } if (temp==2) {
        for (int i = 0; i < 30; i++)
            res=shiftIt(intValue);
    } if (temp==3) {
        for (int i = 0; i < 100; i++)
            res=shiftIt(intValue);
    }
    printf("%d\n", res);
    return res;
}


int modFour(int num) {
    return (num%4);
}
