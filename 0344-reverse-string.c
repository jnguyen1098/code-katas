void reverseString(char *s, int sSize)
{
    char tmp;
    for (int i = 0; i < sSize / 2; i++) {
        char tmp = s[i];
        s[i] = s[sSize - i - 1];
        s[sSize - i - 1] = tmp;
    }
}
