# Addtion of two numbers
class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        foo = {}
        for i, val in enumerate(nums):
            complement = target - val
            if complement in foo:
                return [i, foo[complement]]
            foo[val] = i
