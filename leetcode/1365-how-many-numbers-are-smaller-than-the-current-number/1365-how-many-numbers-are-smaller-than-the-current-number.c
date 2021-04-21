int *smallerNumbersThanCurrent(int *nums, int numsSize, int *returnSize)
{
    int *results = calloc(numsSize, sizeof(int));
    
    for (int i = 0; i < numsSize; i++) {
        for (int j = 0; j < numsSize; j++) {
            if (nums[i] > nums[j] && i != j) {
                results[i]++;
            }
        }
    }
    
    *returnSize = numsSize;
    return results;
}
