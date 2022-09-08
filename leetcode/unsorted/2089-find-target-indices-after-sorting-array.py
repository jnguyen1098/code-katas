class Solution:
    def targetIndices(self, nums: List[int], target: int) -> List[int]:
        nums.sort()
        indices = []
        
        for idx, num in enumerate(nums):
            if num == target:
                indices.append(idx)
        
        return indices
