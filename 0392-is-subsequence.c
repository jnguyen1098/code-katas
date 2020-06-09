bool isSubsequence(char *s, char *t)
{
    for (; *t; s += *s == *t++)
      ;
    return !*s;
}
