char findTheDifference(char *s, char *t)
{
    char counts[26] = {0};
    
    for (int i = 0; s[i]; i++) {
        counts[s[i] - 'a']++;
    }
    
    for (int i = 0; t[i]; i++) {
        counts[t[i] - 'a']--;
    }
    
    for (int i = 0; i < 26; i++) {
        if (counts[i] == -1) {
            return i + 'a';
        }
    }
    
    exit(1);
}
