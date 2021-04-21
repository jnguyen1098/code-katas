/*
    Find the highest index i such that s[i] < s[i+1]. If no such index exists, the permutation is the last permutation.
    Find the highest index j > i such that s[j] > s[i]. Such a j must exist, since i+1 is such an index.
    Swap s[i] with s[j].
    Reverse the order of all of the elements after index i through the last element.
    
    https://stackoverflow.com/questions/1622532/algorithm-to-find-next-greater-permutation-of-a-given-string
*/

int intcmp(const void *a, const void *b)
{
    return *(int *)a - *(int *)b;
}

void nextPermutation(int *s, int numsSize)
{
    int i = -1;
    for (int iter = 0; iter < numsSize - 1; iter++) {
        if (s[iter] < s[iter + 1]) {
            i = iter;
        }
    }
    
    if (i == -1) {
        qsort(s, numsSize, sizeof(int), intcmp);
        return;
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
}
