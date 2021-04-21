#define NUM_LETTERS 26

bool isAnagram(char *s, char *t)
{
    int letters[NUM_LETTERS] = { 0 };
    
    for (int i = 0; s[i]; i++) {
        letters[s[i] - 'a']++;
    }
    
    for (int i = 0; t[i]; i++) {
        letters[t[i] - 'a']--;
    }
    
    for (int i = 0; i < NUM_LETTERS; i++) {
        if (letters[i] != 0) {
            return false;
        }
    }
    
    return true;
}
