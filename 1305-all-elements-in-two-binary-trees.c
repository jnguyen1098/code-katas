int intcmp(const void *a, const void *b)
{
    return *(int *)a - *(int *)b;
}

void peel(struct TreeNode *root, int *coom, int *n)
{
    if (root) {
        coom[(*n)++] = root->val;
        peel(root->left, coom, n);
        peel(root->right, coom, n);
    }
}

int *getAllElements(struct TreeNode *root1, struct TreeNode *root2, int *returnSize)
{
    int *coom = calloc(sizeof(int), 10000);
    int size = 0;
    
    peel(root1, coom, &size);
    peel(root2, coom, &size);
    
    *returnSize = size;
    qsort(coom, size, sizeof(int), intcmp);
    return coom;
}

