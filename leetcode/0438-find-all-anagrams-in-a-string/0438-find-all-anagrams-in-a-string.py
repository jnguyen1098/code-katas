class Solution:
    def findAnagrams(self, string: str, pat_str: str) -> List[int]:
        indexes = []
        window = {}
        pattern = {}
        
        for char in pat_str:
            if char not in pattern:
                pattern[char] = 0
            pattern[char] += 1
            
        window_start = 0
        for window_end in range(len(string)):
            right_char = string[window_end]
            if right_char not in window:
                window[right_char] = 0
            window[right_char] += 1
            
            if window_end >= len(pat_str) - 1:
                if window == pattern:
                    indexes.append(window_start)
                left_char = string[window_start]
                window[left_char] -= 1
                if window[left_char] == 0:
                    window.pop(left_char)
                window_start += 1
        
        return indexes
