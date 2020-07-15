char *reverseWords(char *s)
{
    if (!s) return NULL;
    
    char *word;
    if (!(word = strtok(s, " ")))
        return "";
    
    char *string = malloc(100000);
    *string = 0;
    
    char *words[50000];
    int n = 0;
    
    words[n++] = strcpy(malloc(strlen(word) + 1), word);
    
    while ((word = strtok(NULL, " ")))
        words[n++] = strcpy(malloc(strlen(word) + 1), word);
    
    for (int i = n - 1; i >= 0; i--) {
        strcat(string, words[i]);
        strcat(string, " ");
    }
    
    string[strlen(string) - 1] = 0;
    
    return string;
}
