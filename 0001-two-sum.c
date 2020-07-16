int* twoSum(int* nums, int numsSize, int target, int* returnSize){
    int *to_return = malloc(sizeof(int) * 2);
    *returnSize = 2; // ???
    for (int i = 0; i < numsSize; i++)  {
        for (int j = i + 1; j < numsSize; j++) {
            if ((nums[i] + nums[j]) == target) {
                to_return[0] = i;
                to_return[1] = j;
                return to_return;
            }
        }
    }
    return to_return;
}
