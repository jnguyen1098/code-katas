int maximumWealth(int **accounts, int accountsSize, int *accountsColSize)
{
    int *accs = calloc(accountsSize, sizeof(int));
    for (int i = 0; i < accountsSize; i++) {
        for (int j = 0; j < *accountsColSize; j++) {
            accs[i] += accounts[i][j];
        }
    }
    int max = 0;
    for (int i = 0; i < accountsSize; i++) {
        if (accs[i] > max) {
            max = accs[i];
        }
    }
    return max;
}
