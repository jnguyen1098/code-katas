

bool checkAlmostEquivalent(char *word1, char *word2)
{
    int key[26] = {0};
    
    for (int i = 0; word1[i]; i++) {
        key[word1[i] - 'a']++;
    }
    
    for (int i = 0; word2[i]; i++) {
        key[word2[i] - 'a']--;
    }
    
    int diff = 0;
    
    for (int i = 0; i < 26; i++) {
        if (abs(key[i]) > 3) {
            return false;
        }
    }
    
    return true;
}
