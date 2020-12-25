int calculateTime(char *keyboard, char *word)
{
    int result = 0;
    
    int chars[26] = { 0 };
    for (int i = 0; keyboard[i]; i++) {
        chars[keyboard[i] - 'a'] = i;
    }
    
    int finger = 0;
    for (int i = 0; word[i]; i++) {
        result += abs(finger - chars[word[i] - 'a']);
        finger = chars[word[i] - 'a'];
    }
    
    return result;
}
