int balancedStringSplit(char *s)
{
    int balance = 0;
    int result = 0;
    
    for (int i = 0; s[i]; i++) {
        balance += s[i] == 'R' ? 1 : -1;
        if (balance == 0) {
            result++;
        }
    }
    
    return result;
}
