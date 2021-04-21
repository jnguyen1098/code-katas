class Solution:
    def findDuplicates(self, nums: List[int]) -> List[int]:
        result = defaultdict(int)
        
        for num in nums:
            result[num] += 1
        
        return list(filter(lambda x: result[x] == 2, result.keys()))
