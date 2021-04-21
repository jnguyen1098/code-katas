int numIdenticalPairs(int *nums, int numsSize)
{
    short count = 0;
    
    short ocs[100] = { 0 };
    for (short i = 0; i < numsSize; i++) {
        count += ocs[nums[i] - 1];
        ocs[nums[i] - 1]++;
    }
    
    return (int)count;
}
