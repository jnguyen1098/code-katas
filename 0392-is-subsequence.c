bool isSubsequence(char *s, char *t)
{
    return (({for(;*t;s+=*s==*t++);!*s;}));
}
