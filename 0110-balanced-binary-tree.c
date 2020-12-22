int height(struct TreeNode *root)
{
    if (!root) return 0;
    
    int l_height = height(root->left);
    int r_height = height(root->right);
    
    return l_height > r_height ? l_height + 1: r_height + 1;
}

bool isBalanced(struct TreeNode *root)
{
    return !root ? true : abs(height(root->left) - height(root->right)) <= 1 && isBalanced(root->left) && isBalanced(root->right);
}
