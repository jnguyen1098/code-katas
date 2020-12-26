int reverse(int x)
{
    long result = 0;
    
    while (x) {
        result *= 10;
        result += x % 10;
        x /= 10;
    }
    
    return result <= INT_MAX && result >= -INT_MAX ? (int)result : 0;
}
