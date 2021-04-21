bool isOneBitCharacter(int *bits, int bitsSize)
{
    int i = 0;
    for (; i < bitsSize - 1; i++) {
        if (bits[i] == 1) {
            i++;
        }
    }
    return i + 1 == bitsSize;
}
