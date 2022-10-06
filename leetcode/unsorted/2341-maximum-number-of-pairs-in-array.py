class Solution:
    def numberOfPairs(self, nums: List[int]) -> List[int]:
        counter = Counter(nums)
        
        pairs = 0
        leftovers = 0
        
        for num, freq in counter.items():
            if freq % 2 == 0:
                pairs += (freq // 2)
            else:
                leftovers += 1
                pairs += ((freq - 1) // 2)
        
        return [pairs, leftovers]
