class Solution:
    def numJewelsInStones(self, jewels: str, stones: str) -> int:
        
        counts = defaultdict(int)
        for stone in stones:
            counts[stone] += 1
            
        result = 0
        
        for key, value in counts.items():
            if key in jewels:
                result += value
            
        return result
