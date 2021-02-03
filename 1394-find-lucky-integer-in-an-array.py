class Solution:
    def findLucky(self, arr: List[int]) -> int:
        freqs = defaultdict(int)
        max_lucky = -1
        
        for num in arr:
            freqs[num] += 1
            
        for number, frequency in freqs.items():
            if number == frequency:
                max_lucky = max(max_lucky, number)
        
        return max_lucky
