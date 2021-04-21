int next(int n)
{
    int result = 0;
    
    while (n) {
        result += (n % 10) * (n % 10);
        n /= 10;
    }
    
    return result;
}

bool isHappy(int n)
{
    int fast = n;
    int slow = n;
    
    for (;;) {
        fast = next(next(fast));
        slow = next(slow);
        if (fast == slow) {
            return fast == 1;
        }
    }
}
