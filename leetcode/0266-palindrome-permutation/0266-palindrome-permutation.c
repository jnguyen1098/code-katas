#define NUM_ASCII 128

bool canPermutePalindrome(char *s)
{
    if (!s) return false;
    
    int freqs[NUM_ASCII] = { 0 };
    
    for (char *c = s; *c; c++) {
        freqs[*c]++;
    }
    
    int num_odd = 0;
    
    for (int i = 0; i < NUM_ASCII; i++) {
        if ((freqs[i] % 2)) {
            num_odd++;
        }
    }
    
    return num_odd == 0 || num_odd == 1;
}
