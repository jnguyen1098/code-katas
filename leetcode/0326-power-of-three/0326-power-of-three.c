bool isPowerOfThree(int n)
{
    return n > 0 && !(1162261467 % n);
}

bool isPowerOfThreeLoop(int n)
{
    if (!n) return false;
    
    while (n != 1) {
        if (n % 3 != 0) {
            return false;
        }
        n /= 3;
    }
    
    return true;
}
