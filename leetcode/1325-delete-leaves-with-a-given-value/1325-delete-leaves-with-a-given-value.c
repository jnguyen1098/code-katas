struct TreeNode *removeLeafNodes(struct TreeNode *root, int target)
{
    if (root->left) {
        root->left = removeLeafNodes(root->left, target);
    }
    if (root->right) {
        root->right = removeLeafNodes(root->right, target);
    }
    if (!root->left && !root->right && root->val == target) {
        return NULL;
    }
    return root;
}
