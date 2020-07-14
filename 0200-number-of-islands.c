void excavate(char **grid, int gridSize, int *gridColSize, int i, int j)
{
    grid[i][j] = 48;
    if (i > 0 && grid[i - 1][j] == 49)
        excavate(grid, gridSize, gridColSize, i - 1, j);
    if (i < gridSize - 1 && grid[i + 1][j] == 49)
        excavate(grid, gridSize, gridColSize, i + 1, j);
    if (j > 0 && grid[i][j - 1] == 49)
        excavate(grid, gridSize, gridColSize, i, j - 1);
    if (j < *gridColSize - 1 && grid[i][j + 1] == 49)
        excavate(grid, gridSize, gridColSize, i, j + 1);
}

int numIslands(char **grid, int gridSize, int *gridColSize)
{
    int result = 0;
    
    for (int i = 0; i < gridSize; i++) {
        for (int j = 0; j < *gridColSize; j++) {
            if (grid[i][j] == 49) {
                result++;
                excavate(grid, gridSize, gridColSize, i, j);
            }
        }
    }
    
    return result;
}
