char *interpret(char *command)
{
    char tmp[strlen(command) + 1];
    int n = 0;
    
    for (int i = 0; command[i]; i++) {
        switch (command[i]) {
            case 'G':
                tmp[n++] = 'G';
                break;
            case '(':
                if (command[i + 1] == ')') {
                    tmp[n++] = 'o';
                    i++;
                } else {
                    tmp[n++] = 'a';
                    tmp[n++] = 'l';
                    i += 3;
                }
                break;
        }
    }
    
    tmp[n] = '\0';
    strcpy(command, tmp);
    return command;
}
