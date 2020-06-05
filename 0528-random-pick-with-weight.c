typedef struct {
    int dist_size;
    short max;
    int *left;
} Solution;

Solution *solutionCreate(int *w, int wSize)
{
    Solution *solution = malloc(sizeof(Solution));
    
    int sum = 0;
    for (int i = 0; i < wSize; i++)
        sum += w[i];
    solution->dist_size = sum;
    
    int *left = malloc(sizeof(int) * (wSize + 1));
    solution->max = wSize;
    
    int bookmark = -1;
    for (int i = 0; i < wSize; i++) {
        left[i] = bookmark + 1;
        bookmark += w[i];
    }
    left[wSize] = bookmark + 1;
    
    solution->left = left;
    
    return solution;
}

int solutionPickIndex(Solution *obj)
{
    if (obj->dist_size == 1) return 0;
    
    int l = 0;
    int r = obj->max - 1;
    int target = rand() % obj->dist_size;
    
    while (l <= r) {
        int mid = l + (r - l) / 2;
        
        if (target >= obj->left[mid] && target <= obj->left[mid + 1] - 1)
            return mid;
        
        if (target < obj->left[mid])
            r = mid - 1;
        
        else
            l = mid + 1;
    }
    return -1;
}

void solutionFree(Solution *obj)
{
    free(obj->left);
    free(obj);
}
