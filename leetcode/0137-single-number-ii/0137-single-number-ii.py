class Solution:
    def singleNumber(self, nums: List[int]) -> int:
        freqs = defaultdict(int)
        for num in nums:
            freqs[num] += 1
        for key, value in freqs.items():
            if value == 1:
                return key
