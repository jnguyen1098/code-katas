bool isPowerOfFour(int num)
{
    return          // Assert that. . .
            num > 0 // The number is not 0 (as exponentiation can never reach 0), and that
        && (num & (num - 1)) == 0 // There exists only a single 1 bit in the entire number, and that
        && (num & 0b01010101010101010101010101010101) != 0; // This single 1-bit exists on an even column.
    
    // The last stipulation is needed for the following reasoning:
    // 00000001 =>  1 => Power of 4
    // 00000010 =>  2 => Not a power of 4
    // 00000100 =>  4 => Power of 4
    // 00001000 =>  8 => Not a power of 4
    // 00010000 => 16 => power of 4
    // Powers of 4 occur only at every other column. This is because you need to advance powers of two
    // twice in order to reach a power of 4 (as 2^2 = 4). We use the 0b01010101010101010101010101010101
    // bitmask above in order to ensure that the single one-bit is not within this "power of two" range
}

bool isPowerOfFour_oldsolution(int n)
{
    for (; n; n /= 4) {
        if (n == 1) return true;
        if (n % 4) return false;
    }
    return false;
}
