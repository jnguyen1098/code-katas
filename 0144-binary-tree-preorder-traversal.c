int *traverse(struct TreeNode *root, int *result, int *size)
{
    if (root) {
        result[(*size)++] = root->val;
        traverse(root->left, result, size);
        traverse(root->right, result, size);
    }
    return result;
}

int *preorderTraversal(struct TreeNode *root, int *returnSize)
{
    return traverse(root, malloc(sizeof(int) * 10000), (*returnSize = 0, returnSize));
}
