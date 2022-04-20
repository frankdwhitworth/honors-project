// This is going to do some math 
//   if the given number is even,
//   else, it will just printf

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

int isEven(int num);

int main(int argc, char *argv[]) {
    int i = 0;
    int res = 0;
    int intValue;

    if(argc == 1) {
        printf("Pluf, you forgots the argument for %s \n", argv[0]);
        return 1;
    }

    intValue = atoi(argv[1]);
    //printf("%d\n", intValue);
    if(isEven(intValue)) {
        // printf("The number is even.\n");
        for (i; i < intValue*2; i++) {
            res+= (i*i);
        }
    } else {
        printf("The number is odd.\n");
    }
    return res;
}


int isEven(int num) {
    return !(num & 1);
}
