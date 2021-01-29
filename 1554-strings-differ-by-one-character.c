int wordcmp(const void *a, const void *b)
{
    return strcmp(*(char **)a, *(char **)b);
}

int differ(char *a, char *b)
{
    int diff = 0;
    for (int i = 0; a[i]; i++) {
        if (a[i] != b[i]) {
            if (diff != 0) return false;
            diff = 1;
        }
    }
    return diff == 1;
}

bool differByOne(char **dict, int dictSize)
{
    qsort(dict, dictSize, sizeof(char *), wordcmp);
    
    for (int i = 0; i < dictSize; i++) {
        for (int j = 0; j < dictSize; j++) {
            if (differ(dict[i], dict[j])) {
                return true;
            }
        }
    }
    
    return false;
}
