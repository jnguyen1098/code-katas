int subtractProductAndSum(int n)
{
    int prod = 1;
    int sum = 0;
    
    for (; n; n /= 10) {
        prod *= n % 10;
        sum += n % 10;
    }
    
    return prod - sum;
}
