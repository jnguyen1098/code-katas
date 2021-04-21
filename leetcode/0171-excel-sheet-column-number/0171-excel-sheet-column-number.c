int titleToNumber(char *s)
{
    int result = 0;
    int base = strlen(s) - 1;
    for (; *s; s++)
        result += pow(26, base--) * (*s - 'A' + 1);
    return result;
}
