bool *kidsWithCandies(int *candies, int candiesSize, int extraCandies, int *returnSize)
{
    bool *res = malloc(sizeof(bool) * candiesSize);
    
    int max = *candies;
    for (int i = 1; i < candiesSize; i++)
        max = candies[i] > max ? candies[i] : max;
    
    for (int i = 0; i < candiesSize; i++) {
        res[i] = candies[i] + extraCandies >= max;
    }
    
    *returnSize = candiesSize;
    return res;
}
