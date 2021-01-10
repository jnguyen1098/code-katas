int fib(int n)
{
    if (n == 0) return 0; 
    
    int first = 1;
    int second = 1;
    
    int i;
    for (i = 1; i < n; i++) {
        if (i % 2 == 0) {
            first += second;
        } else {
            second += first;
        }
    }
    
    return i % 2 == 0 ? first : second;
}
