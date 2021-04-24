#include <stdio.h>

void sortColors(int *nums, int numsSize)
{
    int num_zeroes = 0;
    int num_ones = 0;
    int num_twos = 0;
    
    int i = 0;
    
    for (; i < numsSize; i++) {
        switch (nums[i]) {
            case 0:
                num_zeroes++;
                break;
                
            case 1:
                num_ones++;
                break;
                
            case 2:
                num_twos++;
                break;
        }
    }
    
    i = 0;
    while (num_zeroes--)
        nums[i++] = 0;
    
    while (num_ones--)
        nums[i++] = 1;
    
    while (num_twos--)
        nums[i++] = 2;
}

void print_arr(int *nums, int n) {
    for (int i = 0; i < n; i++) {
        printf("%d ", nums[i]);
    }
    puts("");
}

int main(void)
{
    int nums[] = {0, 1, 1, 1, 2, 1, 0, 0, 1, 2};
    int n = sizeof(nums) / sizeof(*nums);
    print_arr(nums, n);
    sortColors(nums, n);
    print_arr(nums, n);
    return 0;
}
