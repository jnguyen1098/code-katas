void backspace(char **bk, char *orig)
{
    if (*bk != orig)
        (*bk)--;
    **bk = 0;
}

bool backspaceCompare(char *a, char *b)
{
    char a_cpy[strlen(a) + 1];
    memset(a_cpy, 0, strlen(a) + 1);
    
    char b_cpy[strlen(b) + 1];
    memset(b_cpy, 0, strlen(b) + 1);
    
    char *curs_a = a_cpy;
    char *curs_b = b_cpy;
    
    for (int i = 0; a[i]; i++) {
        if (a[i] == '#') {
            backspace(&curs_a, a_cpy);
        } else {
            *curs_a = a[i];
            curs_a++;
        }
    }
    
    for (int i = 0; b[i]; i++) {
        if (b[i] == '#') {
            backspace(&curs_b, b_cpy);
        } else {
            *curs_b = b[i];
            curs_b++;
        }
    }
    
    return !strcmp(a_cpy, b_cpy);
}
