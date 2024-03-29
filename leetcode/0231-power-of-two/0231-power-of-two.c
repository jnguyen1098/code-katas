// Explanation:

// 16 = 1000
// 15 = 0111

// 32 = 10000
// 31 = 01111

// Notice how the ones in a power of two and its increment are mutually-exclusive.
// That means if we mask them using &, it should be return 0.

// Of course, we also need to check if the number is positive.

bool isPowerOfTwo(int n)
{
    return n > 0 && !((n & (n - 1)));
}
