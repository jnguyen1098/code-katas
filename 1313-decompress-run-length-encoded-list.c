int *decompressRLElist(int *nums, int numsSize, int *returnSize)
{
    int *res = malloc(100000);
    *returnSize = 0;
    
    for (int i = 0; i < numsSize; i += 2) {
        for (int j = 0; j < nums[i]; j++) {
            res[(*returnSize)++] = nums[i + 1];
        }
    }
    
    return res;
}
