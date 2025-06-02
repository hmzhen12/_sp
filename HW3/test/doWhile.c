#include<stdio.h>

int main (){
    int a,sum;
    a = 0;
    do{
        a++;
        sum = sum + a;
    }while ( a < 10);
    printf("sum(10)=%d\n", sum);
    return 0;
}