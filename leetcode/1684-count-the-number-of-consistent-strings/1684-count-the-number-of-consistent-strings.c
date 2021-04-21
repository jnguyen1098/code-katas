int countConsistentStrings(char *allowed, char **words, int wordsSize)
{
    int count = 0;
    
    int map[26] = { 0 };
    for (int i = 0; allowed[i]; i++) {
        map[allowed[i] - 'a'] = 1;
    }
    
    for (int i = 0; i < wordsSize; i++) {
        int allowed = 1;
        for (int j = 0; words[i][j]; j++) {
            if (map[words[i][j] - 'a'] == 0) {
                allowed = 0;
                break;
            }
        }
        if (allowed) count++;
    }
    
    return count;
}
