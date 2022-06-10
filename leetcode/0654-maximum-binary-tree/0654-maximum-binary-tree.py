class Solution:
    def constructMaximumBinaryTree(self, nums: List[int]) -> Optional[TreeNode]:
        
        def get_max(l, r):
            idx = l
            for i in range(l, r + 1):
                if nums[i] > nums[idx]:
                    idx = i
            return idx
        
        def build_max(l, r):
            if l > r:
                return None
            idx = get_max(l, r)
            root = TreeNode(nums[idx])
            root.left = build_max(l, idx - 1)
            root.right = build_max(idx + 1, r)
            return root
        
        return build_max(0, len(nums) - 1)
