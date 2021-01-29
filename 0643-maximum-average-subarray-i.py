class Solution:
    def findMaxAverage(self, nums: List[int], k: int) -> float:
        
        max_avg = -math.inf
        buf = 0
        
        windowStart = 0
        
        for windowEnd in range(len(nums)):
            buf += nums[windowEnd]
            if windowEnd >= k - 1:
                max_avg = max(max_avg, buf / k)
                buf -= nums[windowStart]
                windowStart += 1
            
        return max_avg
