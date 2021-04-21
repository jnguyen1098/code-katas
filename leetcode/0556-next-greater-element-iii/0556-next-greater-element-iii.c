/*
    Find the highest index i such that s[i] < s[i+1]. If no such index exists, the permutation is the last permutation.
    Find the highest index j > i such that s[j] > s[i]. Such a j must exist, since i+1 is such an index.
    Swap s[i] with s[j].
    Reverse the order of all of the elements after index i through the last element.
    
    https://stackoverflow.com/questions/1622532/algorithm-to-find-next-greater-permutation-of-a-given-string
*/

// Code taken from my #31 solution (next permutation)

int intcmp(const void *a, const void *b)
{
    return *(int *)a - *(int *)b;
}

int nextPermutation(int *s, int numsSize)
{
    int i = -1;
    for (int iter = 0; iter < numsSize - 1; iter++) {
        if (s[iter] < s[iter + 1]) {
            i = iter;
        }
    }
    
    if (i == -1) {
        return 0;
    }
    
    int j = i + 1;
    for (int iter = i + 1; iter < numsSize; iter++) {
        if (s[i] < s[iter]) {
            j = iter;
        }
    }
    
    int tmp_s = s[i];
    s[i] = s[j];
    s[j] = tmp_s;
    
    int rev[numsSize - (i + 1)]; // TODO: reduce size
    int rev_n = 0;
    
    for (int iter = i + 1; iter < numsSize; iter++) {
        rev[rev_n++] = s[iter];
    }
    
    for (int iter = i + 1; iter < numsSize; iter++) {
        s[iter] = rev[--rev_n];
    }
    
    return 1;
}

#define MAX 500
int nextGreaterElement(int n)
{
    int s[MAX], t[MAX];
    int t_n = 0;
    int numsSize = 0;
    
    while (n) {
        s[numsSize++] = n % 10;
        n /= 10;
    }
    
    for (int i = numsSize - 1; i + 1; i--) {
        t[t_n++] = s[i];
    }
    
    if (!nextPermutation(t, numsSize)) {
        return -1;
    }
    
    long ans = 0;
    
    for (int i = 0; i < numsSize; i++) {
        ans *= 10;
        ans += t[i];
    }
    
    return ans > INT_MAX ? -1 : (int)ans;
}
