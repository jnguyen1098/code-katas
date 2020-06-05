typedef struct {
    int dist_size;
    int max;
    int left[10000];
    int right[10000];
} Solution;

int inclrand(int M, int N) // inclusive-inclusive
{
    return M + rand() / (RAND_MAX / (N - M + 1) + 1);
}

Solution *solutionCreate(int *w, int wSize)
{
    Solution *solution;
    if (!(solution = calloc(1, sizeof(Solution))))
        return NULL;
    
    int sum = 0;
    for (int i = 0; i < wSize; i++)
        sum += w[i];
    solution->dist_size = sum;
    

    solution->max = wSize;
    
    int bookmark = -1;
    for (int i = 0; i < wSize; i++) {
        solution->left[i] = bookmark + 1;
        solution->right[i] = bookmark + w[i];
        bookmark += w[i];
    }
    
    srand(time(NULL));
    return solution;
}

int search(int *left, int *right, int size, int target)
{
    for (int i = 0; i < size; i++) {
        if (target >= left[i] && target <= right[i])
            return i;
    }
    return -1;
}

int solutionPickIndex(Solution *obj)
{
    if (!(obj->dist_size - 1)) return 0;
    int start = inclrand(0, obj->dist_size - 1);
    return search(obj->left, obj->right, obj->max, start);
    return -1;
}

void solutionFree(Solution *obj)
{
    free(obj);
}
