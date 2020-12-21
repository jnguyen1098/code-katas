int strStr(char *haystack, char *needle)
{
    int lim = strlen(haystack) - strlen(needle) + 1;
    
    int k = strlen(needle);
    
    for (int i = 0; i < lim; i++) {
        if (!memcmp(haystack + i, needle, k)) {
            return i;
        }
    }
    
    return -1;
}
