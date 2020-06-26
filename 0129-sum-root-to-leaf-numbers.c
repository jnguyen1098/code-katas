int climb(struct TreeNode *head, int sum)
{
    if (!head) return 0;
    
    if (!head->left && !head->right) {
        return sum + head->val;
    }
    
    sum += head->val;
    sum *= 10;
    
    int left = head->left ? climb(head->left, sum) : 0;
    int right = head->right ? climb(head->right, sum) : 0;
    
    return left + right;
}

int sumNumbers(struct TreeNode *root)
{
    return climb(root, 0);
}
