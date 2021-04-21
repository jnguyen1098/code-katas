class Solution:
    def singleNumber(self, nums: List[int]) -> int:
        missing = 0
        
        for num in nums:
            missing ^= num
        
        return missing
