char *removeOuterParentheses(char *S)
{
    char *result = calloc(1, strlen(S) + 1);
    int n = 0;
    int cnt = 0;
    for (int i = 0; S[i]; i++) {
        
        if (cnt == 0 && S[i] == '(') {
            if (S[i] == '(') cnt++;
            if (S[i] == ')') cnt--;
            continue;
        }
        
        if (S[i] == '(') cnt++;
        if (S[i] == ')') cnt--;
        
        if (cnt == 0 && S[i] == ')') {
            continue;
        }
        
        result[n++] = S[i];
    }
    return result;
}
