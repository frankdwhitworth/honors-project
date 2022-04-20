/* Header file for 
 * four_choice.c
 *
 * 2/22/2022 (two's day on a tuesday)
 *
 */
 
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <math.h>
#include <unistd.h> /* for fork */
#include <sys/types.h> /* for pid_t */
#include <sys/wait.h> /* for wait */
#include <limits.h>
#include <stdbool.h>

#define V 9

int forkIt();
int readIt();
int log10It(int num);
int binaryIt(int num);
int foo(int arr[], int l, int r, int x);
int dynamicIt(int intValue);
int expIt(int num);
void dijkstra(int graph[V][V], int src);
int minDistance(int dist[], bool sptSet[]);
void printSolution(int dist[]);
// int matrixIt(int num);

// Number of vertices in the graph

 
// A utility function to find the vertex with minimum distance value, from
// the set of vertices not yet included in shortest path tree
int minDistance(int dist[], bool sptSet[])
{
    // Initialize min value
    int min = INT_MAX, min_index;
 
    for (int v = 0; v < V; v++)
        if (sptSet[v] == false && dist[v] <= min)
            min = dist[v], min_index = v;
 
    return min_index;
}
 
// A utility function to print the constructed distance array
void printSolution(int dist[])
{
    printf("Vertex \t\t Distance from Source\n");
    for (int i = 0; i < V; i++)
        printf("%d \t\t %d\n", i, dist[i]);
}
 
// Function that implements Dijkstra's single source shortest path algorithm
// for a graph represented using adjacency matrix representation
void dijkstra(int graph[V][V], int src)
{
    int dist[V]; // The output array.  dist[i] will hold the shortest
    // distance from src to i
 
    bool sptSet[V]; // sptSet[i] will be true if vertex i is included in shortest
    // path tree or shortest distance from src to i is finalized
 
    // Initialize all distances as INFINITE and stpSet[] as false
    for (int i = 0; i < V; i++)
        dist[i] = INT_MAX, sptSet[i] = false;
 
    // Distance of source vertex from itself is always 0
    dist[src] = 0;
 
    // Find shortest path for all vertices
    for (int count = 0; count < V - 1; count++) {
        // Pick the minimum distance vertex from the set of vertices not
        // yet processed. u is always equal to src in the first iteration.
        int u = minDistance(dist, sptSet);
 
        // Mark the picked vertex as processed
        sptSet[u] = true;
 
        // Update dist value of the adjacent vertices of the picked vertex.
        for (int v = 0; v < V; v++)
 
            // Update dist[v] only if is not in sptSet, there is an edge from
            // u to v, and total weight of path from src to  v through u is
            // smaller than current value of dist[v]
            if (!sptSet[v] && graph[u][v] && dist[u] != INT_MAX
                && dist[u] + graph[u][v] < dist[v])
                dist[v] = dist[u] + graph[u][v];
    }
 
    // print the constructed distance array
    printSolution(dist);
}

int dijkstraIt(int num) {
    int graph[V][V] = { { 0, 4, 0, 0, 0, 0, 0, 8, 0 },
                        { 4, 0, 8, 0, 0, 0, 0, 11, 0 },
                        { 0, 8, 0, 7, 0, 4, 0, 0, 2 },
                        { 0, 0, 7, 0, 9, 14, 0, 0, 0 },
                        { 0, 0, 0, 9, 0, 10, 0, 0, 0 },
                        { 0, 0, 4, 14, 10, 0, 2, 0, 0 },
                        { 0, 0, 0, 0, 0, 2, 0, 1, 6 },
                        { 8, 11, 0, 0, 0, 0, 1, 0, 7 },
                        { 0, 0, 2, 0, 0, 0, 6, 7, 0 } };
 
    dijkstra(graph, num);
 
    return 0;
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
    return (int)sqrt(num);
}

int binaryIt(int num) {
    int arr[100];
    for (int i = 0; i < 100; i++) {
        arr[i] = (rand() % 64);
        printf("%d\n", arr[i]);
    }
    int n = sizeof(arr) / sizeof(arr[0]);
    int x = num;
    int res = foo(arr, 0, n-1, x);
    return res;
}

int foo(int arr[], int l, int r, int x) {
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

// int shiftIt(int num) {
//     int res = 0;
//     int i = 0;
//     for (i; i < num%3; i++)
//         res = num >> i/2;
//     return res;
// }

int shiftIt(int num) {
  int a[10][10], b[10][10], sum[10][10], r, c, i, j, k, running_total;
  int temp = num+1;
  running_total = 0;
  r = 3;
  c = 3;
  a[0][0] = 12;
  a[0][1] = 3;
  a[0][2] = 9;
  a[1][0] = 7;
  a[1][1] = 2;
  a[1][2] = 6;
  a[2][0] = 2;
  a[2][1] = 9;
  a[2][2] = 8;

  b[0][0] = 8;
  b[0][1] = 9;
  b[0][2] = 2;
  b[1][0] = 6;
  b[1][1] = 2;
  b[1][2] = 7;
  b[2][0] = 9;
  b[2][1] = 3;
  b[2][2] = 12;

  printf("addition of the matrix=\n");
  for (i = 0; i < r; i++) {
    for (j = 0; j < c; j++) {
      sum[i][j] = a[i][j] + b[i][j];
    }
  }
  // for printing result
  for (i = 0; i < r; i++) {
    for (j = 0; j < c; j++) {
      printf("%d\t", sum[i][j]);
      running_total += (sum[i][j]/temp) + temp;
    }
    printf("\n");
  }
  printf("running tot=%d\n", running_total);
  return running_total;
}
