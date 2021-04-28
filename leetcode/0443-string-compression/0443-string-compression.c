int compress(char *chars, int charsSize)
{
    int curr_count = 0;
    char curr_char = '\0';
    
    int counts[BUFSIZ] = { 0 };
    int n_cnt = 0;
    
    char keys[BUFSIZ] = { 0 };
    int k_cnt = 0;
    
    for (int i = 0; i < charsSize; i++) {
        if (chars[i] != curr_char) {
            if (curr_count) {
                counts[n_cnt++] = curr_count;
                keys[k_cnt++] = curr_char;
            }
            curr_char = chars[i];
            curr_count = 1;
        } else {
            curr_count++;
        }
    }
    counts[n_cnt++] = curr_count;
    keys[k_cnt++] = curr_char;
    
    int n = 0;
    
    for (int i = 0; i < n_cnt; i++) {
        chars[n++] = keys[i];
        if (counts[i] != 1) {
            if (counts[i] < 10) chars[n++] = counts[i] + '0';
            else n += sprintf(chars + n, "%d", counts[i]);
        }
    }
    
    return n;
}
