/**
 * Definition for a binary tree node.
 * struct TreeNode {
 *     int val;
 *     TreeNode *left;
 *     TreeNode *right;
 *     TreeNode() : val(0), left(nullptr), right(nullptr) {}
 *     TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
 *     TreeNode(int x, TreeNode *left, TreeNode *right) : val(x), left(left), right(right) {}
 * };
 */

vector<vector<int>> printLevelOrder(TreeNode *root)  
{
    if (root == NULL) return {};  
  
    queue<TreeNode *> q;  
    vector<vector<int>> result;
    q.push(root);  
  
    while (q.empty() == false)  
    {  
        int nodeCount = q.size();
        vector<int> row;
        while (nodeCount > 0) 
        {  
            TreeNode *node = q.front();
            row.push_back(node->val);
            
            q.pop();  
            if (node->left != NULL)  
                q.push(node->left);  
            if (node->right != NULL)  
                q.push(node->right);  
            nodeCount--;  
        }
        result.push_back(row);
    }
    std::reverse(result.begin(), result.end());
    return result;
}

class Solution {
public:
    vector<vector<int>> levelOrderBottom(TreeNode* root) {
        return printLevelOrder(root);
    }
};
