int islandPerimeter(int **grid, int gridSize, int *gridColSize)
{
    int perimeter = 0;
    int height = gridSize;
    int width = *gridColSize;
    
    for (int i = 0; i < height; i++) {
        for (int j = 0; j < width; j++) {
            if (grid[i][j]) {
                perimeter += 4;
                if (i - 1 >= 0 && grid[i - 1][j])
                    perimeter--;
                if (i + 1 < height && grid[i + 1][j])
                    perimeter--;
                if (j + 1 < width && grid[i][j + 1])
                    perimeter--;
                if (j - 1 >= 0 && grid[i][j - 1])
                    perimeter--;
            }
        }
    }
    
    return perimeter;
}
