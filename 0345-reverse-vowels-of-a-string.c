#define IS_VOWEL(c)(c == 'a' || c == 'e' || c == 'i' || c == 'o' || c == 'u' ||\
        c == 'A' || c == 'E' || c == 'I' || c == 'O' || c == 'U')

char *reverseVowels(char *s)
{
    int n = 0;
    char *vowels = malloc(strlen(s));
    
    for (int i = 0; s[i]; i++) {
        if (IS_VOWEL(s[i])) {
            vowels[n++] = s[i];
        }
    }
    
    for (int i = 0; s[i]; i++) {
        if (IS_VOWEL(s[i])) {
            s[i] = vowels[--n];
        }
    }
    
    return s;
}
