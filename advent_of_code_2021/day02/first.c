#include <stdio.h>
#include <stdlib.h>

// 984716 1991

int main(void)
{
    FILE *input = fopen("input", "r");
    int x = 0, y = 0, aim = 0;
    for (char buf[BUFSIZ]; fgets(buf, BUFSIZ, input); ) {
        aim += atoi(&buf[2 + (int [128]){[117]=0, [100]=2, [102]=5}[*buf]]) * (int[128]){[100]=1, [117]=0, [102]=0}[*buf];
        aim -= atoi(&buf[2 + (int [128]){[117]=0, [100]=2, [102]=5}[*buf]]) * (int[128]){[100]=0, [117]=1, [102]=0}[*buf];
        y += atoi(&buf[2 + (int [128]){[117]=0, [100]=2, [102]=5}[*buf]]) * (int[128]){[117]=0, [100]=0, [102]=1}[*buf];
        x += aim * atoi(&buf[2 + (int [128]){[117]=0, [100]=2, [102]=5}[*buf]]) * (int[128]){[117]=0, [100]=0, [102]=1}[*buf];
    }
    printf("%d %d\n", x, y);
}




