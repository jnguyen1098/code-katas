char **removeComments(char **source, int sourceSize, int *returnSize)
{
    char *program = calloc(10000, sizeof(char));
    for (int i = 0; i < sourceSize; i++) {
        strcat(program, source[i]);
        strcat(program, "\n");
    }
    
    char *copy = calloc(10000, sizeof(char));
    int len = 0;
    
    for (int i = 0; program[i];) {
        if (program[i] == '/' && program[i + 1] == '/') {
            i += 2;
            while (program[i] != '\n') {
                i++;
            }
            continue;
        }
        if (program[i] == '/' && program[i + 1] == '*') {
            i += 2;
            while (program[i] != '*' || program[i + 1] != '/') {
                i++;
            }
            i += 2;
            continue;
        }
        copy[len++] = program[i];
        i++;
    }
    
    char **result = calloc(5000, sizeof(char *));
    for (int i = 0; i < 5000; i++) result[i] = calloc(sizeof(char), 1000);
    int n = 0;
    
    char *tok = strtok(copy, "\n");
    if (tok) {
        strcpy(result[n++], tok);
        while ((tok = strtok(NULL, "\n"))) {
            strcpy(result[n++], tok);
        }
    }
    
    *returnSize = n;
    return result;
}
