int **subsets(int *nums, int numsSize, int *returnSize, int **returnColumnSizes)
{
    int n = pow(2, numsSize);
    int **results = calloc(1, sizeof(int *) * n);
    
    int *columnSizes = malloc(sizeof(int) * n);
    int push = 0;
    
    for (int i = 0; i < n; i++) {
        int col_size = 0;
        int tmp = i;
        while (tmp) {
            if (tmp & 1)
                col_size++;
            tmp /= 2;
        }
        int *row = malloc(sizeof(int) * col_size);
        
        tmp = i;
        int row_push = 0;
        for (int j = 0; tmp; j++) {
            if (tmp & 1) {
                row[row_push++] = nums[j];
            }
            tmp /= 2;
        }
        
        results[i] = row;
        columnSizes[push++] = col_size;
    }
    
    
    *returnColumnSizes = columnSizes;
    *returnSize = n;
    return results;
}
