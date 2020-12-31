void setZeroes(int **matrix, int matrixSize, int *matrixColSize)
{
    int *rows = calloc(sizeof(int), matrixSize);
    int *cols = calloc(sizeof(int), (*matrixColSize));
    
    for (int i = 0; i < matrixSize; i++) {
        if (rows[i] == 1) continue;
        for (int j = 0; j < *matrixColSize; j++) {
            if (matrix[i][j] == 0) {
                rows[i] = 1;
                cols[j] = 1;
                break;
            }
        }
    }
    
    for (int i = 0; i < *matrixColSize; i++) {
        if (cols[i] == 1) continue;
        for (int j = 0; j < matrixSize; j++) {
            if (matrix[j][i] == 0) {
                rows[j] = 1;
                cols[i] = 1;
                break;
            }
        }
    }
    
    for (int i = 0; i < matrixSize; i++) {
        if (rows[i] == 1) {
            for (int j = 0; j < *matrixColSize; j++) {
                matrix[i][j] = 0;
            }
        }
    }
    
    for (int i = 0; i < *matrixColSize; i++) {
        if (cols[i] == 1) {
            for (int j = 0; j < matrixSize; j++) {
                matrix[j][i] = 0;
            }
        }
    }
}
