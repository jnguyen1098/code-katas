int removeElement(int *nums, int numsSize, int val)
{
    int p = 0;
    int i = 0;
    for (; i < numsSize; i++) {
        if (nums[i] != val) {
            nums[p++] = nums[i];
        }
    }
    return p;
}
