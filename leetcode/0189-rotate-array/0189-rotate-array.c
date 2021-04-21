void rotate(int *nums, int numsSize, int k)
{
    if (k && nums) {
        int n = numsSize - (k % numsSize) - 1;
        
        int *tmp = malloc(sizeof(int) * numsSize);
        memcpy(tmp, nums, numsSize * sizeof(int));
        
        for (int i = 0; i < numsSize; i++) {
            nums[i] = tmp[++n % numsSize];
            n %= numsSize;
        }
    }
}
