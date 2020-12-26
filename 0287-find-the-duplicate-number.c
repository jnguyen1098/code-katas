int findDuplicate(int *nums, int numsSize)
{
    int slow = 0;
    int fast = 0;
    
    for (;;) {
        slow = nums[slow];
        fast = nums[nums[fast]];
        
        if (slow == fast)
            break;
    }
    
    fast = 0;
    for (;;) {
        fast = nums[fast];
        slow = nums[slow];
        
        if (fast == slow)
            return fast;
    }
}
