int countNegatives(int **grid, int gridSize, int *gridColSize)
{
    short count = 0;
    
    for (short i = 0; i < gridSize; i++)
        for (short j = 0; j < *gridColSize; j++)
            if (grid[i][j] < 0)
                count++;
    
    return count;
}
