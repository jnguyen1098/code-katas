bool uniform(char *str)
{
    if (!str) {
        return false;
    }
    
    char tmp = *str;
    
    for (int i = 0; str[i]; i++) {
        if (str[i] != tmp) {
            return false;
        }
    }
    
    return true;
}

int charcmp(const void *a, const void *b)
{
    return *(char *)a - *(char *)b;
}

bool buddyStrings(char *A, char *B)
{
    if (!A || !B || (!*A && !*B)) {
        return false;
    }
    
    if (strlen(A) != strlen(B)) {
        return false;
    }
    
    if (strlen(A) == 1) {
        return false;
    }
    
    if (uniform(A) && uniform(B)) {
        return true;
    }
    
    if (!strcmp(A, B)) {
        char *copy = malloc(strlen(A) + 1);
        strcpy(copy, A);
        int n = strlen(copy);
        qsort(copy, n, 1, charcmp);
        for (int i = 0; i < n - 1; i++) {
            if (copy[i] == copy[i + 1]) {
                return true;
            }
        }
    }
    
    int wrong = 0;
    for (int i = 0; A[i]; i++) {
        if (A[i] != B[i]) {
            wrong++;
        }
    }
    
    if (wrong != 2) {
        return false;
    }
    
    int wrongs[2];
    int n = 0;
    for (int i = 0; A[i]; i++) {
        if (A[i] != B[i]) {
            wrongs[n++] = i;
        }
    }
    
    char tmp = A[wrongs[0]];
    A[wrongs[0]] = A[wrongs[1]];
    A[wrongs[1]] = tmp;
    
    return !strcmp(A, B);
}
