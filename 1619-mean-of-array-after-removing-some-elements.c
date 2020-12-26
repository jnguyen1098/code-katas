int intcmp(const void *a, const void *b)
{
    return *(int *)a - *(int *)b;
}

double trimMean(int *arr, int arrSize)
{
    qsort(arr, arrSize, sizeof(int), intcmp);
    int n = arrSize;
    for (int i = 0; i < arrSize * 0.05; i++) {
        arr[i] = 0;
        n--;
    }
    for (int i = arrSize * 0.95; i < arrSize; i++) {
        arr[i] = 0;
        n--;
    }
    int sum = 0;
    for (int i = 0; i < arrSize; i++) {
        sum += arr[i];
    }
    return (double)sum / (double)n;
}
