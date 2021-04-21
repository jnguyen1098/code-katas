int *shuffle(int *nums, int numsSize, int n, int *returnSize)
{
    
    int *res = malloc(2 * n * sizeof(int));
    int res_n = 0;
    
    int i = 0;
    int j = n;
    
    while (i < n) {
        res[res_n++] = nums[i++];
        res[res_n++] = nums[j++];
    }
    
    *returnSize = 2 * n;
    return res;
}
