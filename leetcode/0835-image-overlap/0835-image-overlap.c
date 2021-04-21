int count_overlap(int **A, int ASize, int **B, int v, int h)
{
    int count = 0;
    
    for (int i = 0; i < ASize; i++) {
        for (int j = 0; j < ASize; j++) {
            if (i - v >= 0 && i - v < ASize && j - h >= 0 && j - h < ASize) {
                if (A[i - v][j - h] == 1 && B[i][j] == 1) {
                    count++;
                }
            }
        }
    }
    
    return count;
}

#define MAX(A, B)(A > B ? A : B)

int largestOverlap(int **A, int ASize, int *AColSize, int **B, int BSize, int *BColSize)
{
    int count = 0;
    
    for (int i = -ASize + 1; i < ASize; i++) {
        for (int j = -ASize + 1; j < ASize; j++) {
            count = MAX(count, count_overlap(A, ASize, B, i, j));
        }
    }
    
    return count;
}
