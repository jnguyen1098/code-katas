int intcmp(const void *a, const void *b) { return *(int *)a - *(int *)b; }

int maxIceCream(int *costs, int costsSize, int coins)
{
    qsort(costs, costsSize, sizeof(int), intcmp);
    int total = 0;
    for (int i = 0; i < costsSize; i++) {
        if (coins - costs[i] >= 0) {
            coins -= costs[i];
            total++;
        } else break;
    }
    return total;
}
