int countAsterisks(char *s)
{
    bool count_asterisks = true;
    
    int count = 0;
    
    for (int i = 0; s[i]; i++) {
        if (s[i] == '|') {
            count_asterisks = !count_asterisks;
        }
        else if (s[i] == '*') {
            count += count_asterisks;
        }
    }
    
    return count;
}
