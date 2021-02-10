int pivotIndex(int *nums, int numsSize)
{
    int right_sum[numsSize];
    right_sum[numsSize - 1] = nums[numsSize - 1];
    for (int i = numsSize - 2; i >= 0; i--) {
        right_sum[i] = nums[i] + right_sum[i + 1];
    }
    
    int running = 0;
    for (int i = 0; i < numsSize; i++) {
        running += nums[i];
        if (running == right_sum[i]) {
            return i;
        }
    }
    
    return -1;
}
