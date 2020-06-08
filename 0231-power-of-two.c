// 16 = 1000
// 15 = 0111

// 32 = 10000
// 31 = 01111

// Notice how the ones are mutually exclusive. If we mask them using &, it should be return 0.

bool isPowerOfTwo(int n)
{
    return n > 0 && !((n & (n - 1)));
}
