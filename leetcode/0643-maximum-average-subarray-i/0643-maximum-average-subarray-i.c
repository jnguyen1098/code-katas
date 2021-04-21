#define MAX(x,y)(x > y ? x : y)
double findMaxAverage(int *nums, int numsSize, int k)
{
    double result = -INFINITY;
    double buf = 0.0;
    
    int windowStart = 0;
    for (int windowEnd = 0; windowEnd < numsSize; windowEnd++) {
        buf += nums[windowEnd];
        if (windowEnd >= k - 1) {
            result = MAX(result, buf / (double)k);
            buf -= nums[windowStart];
            windowStart++;
        }
    }
    
    return result;
}
