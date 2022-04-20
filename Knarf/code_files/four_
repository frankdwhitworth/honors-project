// This is going to do modular 4 a 
//   given number and do something in result

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <math.h>
#include <unistd.h> /* for fork */
#include <sys/types.h> /* for pid_t */
#include <sys/wait.h> /* for wait */


int modFour(int num);
int forkIt();
int readIt();
int log10It(int num);
int binaryIt(int num);
int binarySearch(int arr[], int l, int r, int x);
int dynamicIt(int intValue);
int expIt(int num);

int main(int argc, char *argv[]) {
    int i = 0;
    int res = 0;
    int temp = 4;
    int intValue;

    // if(argc == 1) {
    //     printf("Pluf, you forgots the argument for %s \n", argv[0]);
    //     return 1;
    // }

    intValue = atoi(argv[1]);
    //printf("%d\n", intValue);
    temp = modFour(intValue);
    // printf("%d\n", temp);
    printf("temp=%d\n", temp);
    if (temp==0) {
       	res = readIt();
    } if (temp==1) {
        res = log10It(intValue);
    } if (temp==2) {
        res = dynamicIt(intValue); 
    } if (temp==3) {
        res = binaryIt(intValue);
    }
    printf("%d\n", res);
    return res;
}


int modFour(int num) {
    return (num%4);
}

int forkIt() {
    pid_t pid=fork();
    if (pid==0) { /* child process */
        static char *argv[]={"echo","Foo is my name.",NULL};
        execv("/bin/echo",argv);
        exit(127); /* only if execv fails */
    } else { /* pid!=0; parent process */
        waitpid(pid,0,0); /* wait for child to exit */
    }
    return 0;
}

int readIt() {
    int num;
    int res;
    FILE *fptr;
    if ((fptr = fopen("/home/whitfd18/Knarf/read_this.txt","r")) == NULL){
        printf("Error! opening file");
        // Program exits if the file pointer returns NULL.
        exit(1);
    }
    fscanf(fptr,"%d", &num);
    // printf("Value of n=%d", num);
    fclose(fptr); 
    res = num;
    return res;
}

int writeIt() {
    int num;
    int res;
    FILE *fptr;
    // use appropriate location if you are using MacOS or Linux
    fptr = fopen("/home/whitfd18/Knarf/Outputs/writer.text","w");
    if(fptr == NULL) {
        printf("Error!");   
        exit(1);             
    }
    fprintf(fptr,"%d",num);
    fclose(fptr);
    return 0;
}

int log10It(int num) {
    return (int)log10(num);
}

int binaryIt(int num) {
    int arr[100];
    for (int i = 0; i < 100; i++) {
        arr[i] = (rand() % 64);
        printf("%d\n", arr[i]);
    }
    int n = sizeof(arr) / sizeof(arr[0]);
    int x = num;
    int res = binarySearch(arr, 0, n-1, x);
    return res;
}

int binarySearch(int arr[], int l, int r, int x) {
    while (l <= r) {
        int m = l + (r - l) / 2;
        if (arr[m] == x)
            return m;
        if (arr[m] < x)
            l = m + 1;
        else
            r = m - 1;
    }
    return -1;
}

int dynamicIt(int intValue) {
    double* p;  
    int i;
    p = calloc(intValue, sizeof(double) );  
	for (i = 0; i < intValue; i++) 
	   p[i] = (intValue/(i+1)) * p[i-1];
	srand(0);
    int res = p[intValue%i];
    free(p);
    return res;
}

int expIt(int num) {
    int res;
    for (int i; i < num*3; i++) 
        res += (i*i);
    return res;
}