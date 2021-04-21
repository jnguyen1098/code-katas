int sumOfDigits(int *A, int ASize)
{
    int min = INT_MAX;
    for (int i = 0; i < ASize; i++) {
        min = min > A[i] ? A[i] : min;
    }
    
    int num = 0;
    
    while (min) {
        num += min % 10;
        min /= 10;
    }
    
    return !(num & 1);
}
