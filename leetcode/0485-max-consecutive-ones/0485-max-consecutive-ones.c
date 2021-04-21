int findMaxConsecutiveOnes(int *nums, int numsSize)
{
    int max_ones = 0;
    int ones = 0;
    
    for (int i = 0; i < numsSize; i++, ones++) {
        if (nums[i] == 0) {
            max_ones = ones > max_ones ? ones : max_ones;
            ones = 0;
        } else {
            ones++;
        }
    }
    
    max_ones = ones > max_ones ? ones : max_ones;
    
    return max_ones;
}
