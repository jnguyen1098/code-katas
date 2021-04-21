char *restoreString(char *s, int *indices, int indicesSize)
{
    char *res = calloc(1, strlen(s) + 1);
    
    for (int i = 0; s[i]; i++) {
        res[indices[i]] = s[i];
    }
    
    return res;
}
