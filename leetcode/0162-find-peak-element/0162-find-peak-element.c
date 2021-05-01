int is_peak(int *nums, int i)
{
    return nums[i] > nums[i + 1] && nums[i] > nums[i - 1];
}

int findPeakElement(int *nums, int numsSize)
{
    if (numsSize == 1 || nums[0] > nums[1]) return 0;
    for (int i = 1; i < numsSize - 1; i++) {
        if (is_peak(nums, i)) {
            return i;
        }
    }
    return numsSize - 1;
}
