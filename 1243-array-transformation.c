int *transformArray(int *arr, int arrSize, int *returnSize)
{
    for (;;) {
        int action = 0;
        int *act = calloc(sizeof(int), arrSize);
        for (int i = 1; i < arrSize - 1; i++) {
            if (arr[i] < arr[i - 1] && arr[i] < arr[i + 1]) {
                act[i] = 1;
                action = 1;
            } else if (arr[i] > arr[i - 1] && arr[i] > arr[i + 1]) {
                act[i] = -1;
                action = 1;
            }
        }
        if (!action) {
            *returnSize = arrSize;
            return arr;
        }
        for (int i = 0; i < arrSize; i++) {
            if (act[i] == 1) {
                arr[i]++;
            } else if (act[i] == -1) {
                arr[i]--;
            }
        }
    }
    
    *returnSize = arrSize;
    return arr;
}
