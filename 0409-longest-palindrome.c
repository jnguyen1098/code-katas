#define NUM_ASCII 128

#define MAX(a, b) (a > b ? a : b)

int longestPalindrome(char *s)
{    
    int freqs[NUM_ASCII] = { 0 };
    
    for (char *c = s; *c; c++) {
        freqs[*c]++;
    }
    
    int result = 0;
    int has_odd = 0;
    
    for (int i = 0; i < NUM_ASCII; i++) {
        if (freqs[i] % 2 == 0) {
            result += freqs[i];
        } else {
            result += freqs[i] - 1;
            has_odd = 1;
        }
    }
    
    return result + has_odd;
}
