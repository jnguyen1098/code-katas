int rangeSumBST(struct TreeNode *root, int low, int high)
{
    if (!root) return 0;
    int result = 0;
    
    result += root->val >= low && root->val <= high ? root->val : 0;
    
    return result + rangeSumBST(root->left, low, high) + rangeSumBST(root->right, low, high);
}
