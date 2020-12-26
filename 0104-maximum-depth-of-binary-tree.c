int maxDepth(struct TreeNode* root)
{
    if (root) {
        int l_depth = maxDepth(root->left);
        int r_depth = maxDepth(root->right);
        return 1 + (l_depth > r_depth ? l_depth : r_depth);
    }
    return 0;
}
