int max_depth(struct TreeNode *root)
{
    if (!root) {
        return 0;
    }
    int l = max_depth(root->left);
    int r = max_depth(root->right);
    return (l > r ? l : r) + 1;
}

void traverse(struct TreeNode *root, int level, int target_depth, int *sum)
{
    if (!root) return;
    
    if (level + 1 == target_depth) {
        *sum += root->val;
        return;
    }
    
    traverse(root->left, level + 1, target_depth, sum);
    traverse(root->right, level + 1, target_depth, sum);
}

int deepestLeavesSum(struct TreeNode *root)
{
    int sum = 0;
    traverse(root, 0, max_depth(root), &sum);
    return sum;
}
