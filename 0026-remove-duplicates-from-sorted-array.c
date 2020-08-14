int removeDuplicates(int *nums, int numsSize)
{
    size_t size = numsSize;
    for (int i = 0, j = 1; j < numsSize && i < numsSize; j++) {
        if (nums[i] != nums[j]) {
            nums[++i] = nums[j];
        } else {
            size--;
        }
    }
    return size;
}
