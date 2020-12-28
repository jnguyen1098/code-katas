bool isPowerOfFour(int n)
{
    for (; n; n /= 4) {
        if (n == 1) return true;
        if (n % 4) return false;
    }
    return false;
}
