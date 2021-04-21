int minDepth(struct TreeNode *root)
{
    if (!root) {
        return 0;
    }
    
    if (!root->right) {
        return minDepth(root->left) + 1;
    }
    
    if (!root->left) {
        return minDepth(root->right) + 1;
    }
    
    int left_count = minDepth(root->left);
    int right_count = minDepth(root->right);
    
    return left_count > right_count ? right_count + 1 : left_count + 1;
}
