#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX(x,y)((x)>(y)?(x):(y))

int main(void)
{
    char numbuf[100] = "";
    fgets(numbuf, 100, stdin);
    int n = atoi(numbuf);
    int count[101] = {0};
    char buf[5000] = "";
    fgets(buf, 5000, stdin);
    char *str = strtok(buf, " ");
    for (int i = 0; i < n; i++) {
        if (!str) {
            break;
        }
        count[atoi(str)]++;
        str = strtok(NULL, " ");
    }

    int max = 0;

    for (int i = 1; i <= 100; i++) {
        max = MAX(max, count[i]);
    }

    printf("%d\n", max);
}
