bool isSameTree(struct TreeNode *p, struct TreeNode *q)
{
    if (!p && q || p && !q)
        return false;
    
    if (!p && !q)
        return true;
    
    if (!isSameTree(p->left, q->left) || !isSameTree(p->right, q->right))
        return false;
    
    return p->val == q->val;
}
