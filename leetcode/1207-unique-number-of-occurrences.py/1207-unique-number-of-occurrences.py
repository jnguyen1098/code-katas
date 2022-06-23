class Solution:
    def uniqueOccurrences(self, arr: List[int]) -> bool:
        
        freqs = Counter(arr)
        
        freq_counter = Counter(freqs.values())
        
        for freq, freq_freq in freq_counter.items():
            if freq_freq > 1:
                return False
        
        return True
