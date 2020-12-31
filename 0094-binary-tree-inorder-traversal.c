int *traverse(struct TreeNode *root, int *result, int *size)
{
    if (root) {
        traverse(root->left, result, size);
        result[(*size)++] = root->val;
        traverse(root->right, result, size);
    }
    return result;
}

int *inorderTraversal(struct TreeNode *root, int *returnSize)
{
    return traverse(root, malloc(sizeof(int) * 10000), (*returnSize = 0, returnSize));
}
