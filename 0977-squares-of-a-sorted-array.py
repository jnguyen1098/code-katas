class Solution:
    def sortedSquares(self, nums: List[int]) -> List[int]:
        result = []
        
        for i in range(len(nums)):
            result.append(nums[i] ** 2)
        
        return sorted(result)
