void moveZeroes(int *nums, int numsSize)
{
    int l = 0;
    
    for (int i = 0; i < numsSize; i++) {
        if (nums[i] != 0) {
            nums[l++] = nums[i];
        }
    }
    
    while (l < numsSize)
        nums[l++] = 0;
}
