int hammingDistance(int x, int y)
{
    int d = 0;
    
    while (x || y) {
        d += (x ^ y) & 1;
        x >>= 1;
        y >>= 1;
    }
    
    return d;
}
