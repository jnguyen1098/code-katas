#include <stdio.h>
#include <stdlib.h>
#include <math.h>

int main(void)
{
    long double amount = 0.0;

    int n;
    scanf("%d", &n);

    for (int i = 0; i < n; i++) {
        long double line = 0.0;
        scanf("%Lf", &line);
        amount = fmodl(amount + line, 360.0);
    }

    printf("%.6Lf\n", amount);
}

