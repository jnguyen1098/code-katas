char *longestCommonPrefix(char **strs, int strsSize)
{
    if (!strs || !strsSize || !**strs)
        return "";
    
    char *word = calloc(1, 2500);
    int n = 0;
    
    for (int pos = 0;;pos++) {
    char test = 0;
        for (int i = 0; i < strsSize; i++) {
            if (test == 0) {
                test = strs[i][pos];
                if (test == 0)
                    goto end;
            }
            else {
                if (strs[i][pos] != test)
                    goto end;
            }
        }
        word[n++] = test;
    }
    end:
    word[n++] = 0;
    return word;
}
