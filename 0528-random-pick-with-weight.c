typedef struct {
    int dist_size;
    int max;
    int *left;
    int *right;
} Solution;

Solution *solutionCreate(int *w, int wSize)
{
    Solution *solution = malloc(sizeof(Solution));
    
    int sum = 0;
    for (int i = 0; i < wSize; i++)
        sum += w[i];
    solution->dist_size = sum;
    
    int *left = malloc(sizeof(int) * wSize);
    int *right = malloc(sizeof(int) * wSize);
    solution->max = wSize;
    
    int bookmark = -1;
    for (int i = 0; i < wSize; i++) {
        left[i] = bookmark + 1;
        right[i] = bookmark + w[i];
        bookmark += w[i];
    }
    
    solution->left = left;
    solution->right = right;
    
    srand(time(NULL));
    return solution;
}

int search(int *left, int *right, int l, int r, int target)
{
    int index = (l + r) / 2;
    if (target >= left[index] && target <= right[index]) {
        return index;
    }
    else if (target < left[index]) {
        return search(left, right, 0, index - 1, target);
    }
    else if (target > right[index]) {
        return search(left, right, index + 1, r, target);
    }
    return -1;
}

int solutionPickIndex(Solution *obj)
{
    if (!(obj->dist_size - 1)) return 0;
    return search(obj->left, obj->right, 0, obj->max - 1, rand() % obj->dist_size);
    return -1;
}

void solutionFree(Solution *obj)
{
    free(obj->left);
    free(obj->right);
    free(obj);
}
