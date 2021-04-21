struct TreeNode *searchBST(struct TreeNode *root, int val)
{
    for (;;) {
        if (!root)                  return NULL;
        if (val == root->val)       return root;
        else if (val > root->val)   root = root->right;
        else                        root = root->left;
    }
}
