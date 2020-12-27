int *twoSum(int *numbers, int numbersSize, int target, int *returnSize)
{
    int *result = malloc(2 * sizeof(int));
    *returnSize = 2;
    
    int l = 0;
    int r = numbersSize - 1;
    
    for (;;) {
        int candidate = numbers[l] + numbers[r];
        if (candidate == target) {
            result[0] = l + 1;
            result[1] = r + 1;
            return result;
        } else if (candidate > target) {
            r--;
        } else {
            l++;
        }
    }
    
    exit(0);
}
