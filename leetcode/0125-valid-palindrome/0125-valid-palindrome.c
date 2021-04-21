bool isPalindrome(char *s)
{
    char *first = calloc(1, strlen(s) + 1);
    int n = 0;
    
    char *second = calloc(1, strlen(s) + 1);
    
    for (int i = 0; s[i]; i++) {
        if (isalnum(s[i])) {
            first[n++] = tolower(s[i]);
        }
    }
    
    n = 0;
    
    for (int i = strlen(first) - 1; i + 1; i--) {
        second[n++] = first[i];
    }
    
    return !strcmp(first, second);
}
