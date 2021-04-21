int table[101][101];

int uniquePaths(int m, int n)
{
    if (m == 1 || n == 1) return 1;
    return table[m][n] == 0 ? table[m][n] = uniquePaths(m - 1, n) + uniquePaths(m, n - 1), table[m][n] : table[m][n];
}
