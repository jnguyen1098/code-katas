struct TreeNode *insertIntoBST(struct TreeNode *root, int val)
{
    if (!root) {
        struct TreeNode *to_return = calloc(1, sizeof(struct TreeNode));
        to_return->val = val;
        return to_return;
    }
    
    if (val > root->val) {
        root->right = insertIntoBST(root->right, val);
        return root;
    }
    
    root->left = insertIntoBST(root->left, val);
    return root;
}
