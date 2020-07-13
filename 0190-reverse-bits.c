uint32_t reverseBits(uint32_t n)
{
    int result = 0;
    for (int i = 0; i < 32; i++, n >>= 1)
        result |= ((n & 1) << (31 - i));
    return result;
}
