class Solution:
    def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
        
        def annotate_tree(tree, parent=None):
            if tree is None:
                return
            tree.parent = parent
            tree.seen = False
            annotate_tree(tree.left, tree)
            annotate_tree(tree.right, tree)
        
        annotate_tree(root)
        
        def backtrace(tree):
            if tree is None:
                return
            if tree.seen:
                return tree
            tree.seen = True
            return backtrace(tree.parent)
        
        backtrace(p)
        return backtrace(q)
