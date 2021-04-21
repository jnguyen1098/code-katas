class Solution:
    def runningSum(self, nums: List[int]) -> List[int]:
        last_sum = 0
        for i, num in enumerate(nums):
            last_sum += num
            nums[i] = last_sum
        return nums
