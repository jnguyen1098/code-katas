int hammingWeight(uint32_t n) {
    char value = 0;
    for (; n; n >>= 1)
        value += n & 1;
    return value;
    
    // if you want to reach 100% memory, you have to cheat
    // and use the built-in gcc macro "__builtin_popcount()"
    // return __builtin_popcount(n);
}
