// Brute force method. TODO: replace with stack method

int next_greater(int *nums, int i, int numsSize)
{
    for (int j = i + 1;; j++) {
        if (j % numsSize == i) {
            return -1;
        }
        if (nums[j % numsSize] > nums[i]) {
            return nums[j % numsSize];
        }
    }
    
    exit(0);
}

int *nextGreaterElements(int *nums, int numsSize, int *returnSize)
{
    int *result = calloc(numsSize, sizeof(int));
    
    for (int i = 0; i < numsSize; i++) {
        result[i] = next_greater(nums, i, numsSize);
    }
    
    *returnSize = numsSize;
    return result;
}
