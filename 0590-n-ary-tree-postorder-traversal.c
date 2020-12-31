int *traverse(struct Node *root, int *result, int *size)
{
    if (root) {
        for (int i = 0; i < root->numChildren; i++) {
            traverse(root->children[i], result, size);
        }
        result[(*size)++] = root->val;
    }
    return result;
}

int *postorder(struct Node *root, int *returnSize)
{
    return traverse(root, malloc(sizeof(int) * 10000), (*returnSize = 0, returnSize));
}
