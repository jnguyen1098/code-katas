void sortColors(int *nums, int numsSize)
{
    int zeroes = 0;
    int ones = 0;
    int twos = 0;
    
    int i = 0;
    
    for (; i < numsSize; i++) {
        switch (nums[i]) {
            case 0:
                zeroes++;
                break;
                
            case 1:
                ones++;
                break;
                
            case 2:
                twos++;
                break;
        }
    }
    
    i = 0;
    while (zeroes--)
        nums[i++] = 0;
    
    while (ones--)
        nums[i++] = 1;
    
    while (twos--)
        nums[i++] = 2;
}
