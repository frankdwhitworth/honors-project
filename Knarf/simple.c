#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

int isInteger(char str[]);

int main(int argc, char *argv[]) {
    int i;
    int res = 0;
    int intValue;

    if(argc == 1) {
        printf("Knarf, you forgots the argument for %s \n", argv[0]);
        return 1;
    }

    if(isInteger(argv[1])) {
        intValue = atoi(argv[1]);
        /*
        printf("%s is an int (%d) \n", argv[1], intValue);
        */
        for(i = 0; i < intValue; i++)
            res += (i*i);
    }
    else {
        /*
        printf("%s is not an int \n", argv[1]);
        res = (int) argv[1][0];
        res = res&1;
        */
        intValue = strlen(argv[1]);    
        for(i = 0; i < intValue; i++){
            if(argv[1][i] == 'a')
                res += 1;
        }
    }
    printf("res %d \n", res);  

    return res;
}


int isInteger(char str[]) {
    int isInt = 1;
    int i = 0;
    if(str[0] == '-') i = 1;  
    for(; isInt && str[i] != '\0'; i++)
        if(!isdigit(str[i]))
            isInt = 0;
    return isInt;
}
