int mySqrt(int x)
{
    if (x == 0) return x;
    
    double result = x / 2.0;
    
    for (int i = 0; i < 50; i++) {
        result = ((x / result) + result) / 2.0;
    }
    
    return (int)result;
}
