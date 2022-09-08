class Solution:
    def divideArray(self, nums: List[int]) -> bool:
        counter = Counter(nums)
        
        for number, count in counter.items():
            if count % 2 == 1:
                return False
        
        return True
