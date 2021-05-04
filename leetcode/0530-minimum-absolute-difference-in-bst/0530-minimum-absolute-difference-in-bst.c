#define MIN(x,y)((x) > (y) ? (y) : (x))

void accumulate(struct TreeNode *root, int *amts, int *n)
{
    if (!root) return;
    amts[(*n)++] = root->val;
    accumulate(root->left, amts, n);
    accumulate(root->right, amts, n);
}

int intcmp(const void *a, const void *b)
{
    return *(int *)a - *(int *)b;
}

int getMinimumDifference(struct TreeNode *root)
{
    int *amts = calloc(10000, sizeof(int));
    int n = 0;
    int min_diff = INT_MAX;
    
    accumulate(root, amts, &n);
    
    qsort(amts, n, sizeof(int), intcmp);
    
    for (int i = 0; i < n - 1; i++) {
        min_diff = MIN(min_diff, amts[i + 1] - amts[i]);
    }
    
    return min_diff;
}
