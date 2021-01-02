bool judgeCircle(char *moves)
{
    int ups = 0;
    int downs = 0;
    int lefts = 0;
    int rights = 0;
    
    for (int i = 0; moves[i]; i++) {
        switch (moves[i]) {
            case 'U':
                ups++;
                break;
            case 'D':
                downs++;
                break;
            case 'L':
                lefts++;
                break;
            case 'R':
                rights++;
                break;
        }
    }
    
    return ups == downs && lefts == rights;
}

