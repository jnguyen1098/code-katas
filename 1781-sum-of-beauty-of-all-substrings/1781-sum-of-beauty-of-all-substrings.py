class Solution:
    def beautySum(self, s: str) -> int:
        beauty = 0
        
        def add_beauty(freqs):
            nonlocal beauty
            highest = -math.inf
            lowest = math.inf
            for key, value in freqs.items():
                highest = max(highest, value)
                lowest = min(lowest, value)
            beauty += highest - lowest
        
        for window_size in range(3, len(s) + 1):
            l = 0
            freqs = defaultdict(int)
            for r in range(len(s)):
                freqs[s[r]] += 1
                if r - l + 1 >= window_size:
                    add_beauty(freqs)
                    freqs[s[l]] -= 1
                    if freqs[s[l]] == 0:
                        freqs.pop(s[l])
                    l += 1
        
        return beauty
