int firstUniqChar(char *s)
{
    int map[26] = { 0 };
    
    for (int i = 0; s[i]; i++) {
        map[s[i] -'a']++;
    }
    
    for (int i = 0; s[i]; i++) {
        if (map[s[i] - 'a'] == 1) {
            return i;
        }
    }
    
    return -1;
}
