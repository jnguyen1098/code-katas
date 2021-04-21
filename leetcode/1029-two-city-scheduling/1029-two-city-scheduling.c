int intcmp(const void *a, const void *b)
{
    int *first = *(int **)a;
    int *second = *(int **)b;
    
    return (first[0] - first[1]) - (second[0] - second[1]);
}

int twoCitySchedCost(int **costs, int costsSize, int *costsColSize)
{
    int sum = 0;
    
    qsort(costs, costsSize, sizeof(int *), intcmp);
    
    for (int i = 0; i < costsSize / 2; i++) {
        sum += costs[i][0];
    }
    
    for (int i = costsSize - 1; i >= costsSize / 2; i--) {
        sum += costs[i][1];
    }
    
    return sum;
}
