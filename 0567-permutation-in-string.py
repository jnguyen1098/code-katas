class Solution:
    def checkInclusion(self, str1: str, str2: str) -> bool:
        
        window = {}
        pattern = {}
        
        for char in str1:
            if char not in pattern:
                pattern[char] = 0
            pattern[char] += 1
            
        window_start = 0
        for window_end in range(len(str2)):
            
            if str2[window_end] not in window:
                window[str2[window_end]] = 0
            window[str2[window_end]] += 1
            
            if window_end >= len(str1) - 1:
                if window == pattern:
                    return True
                window[str2[window_start]] -= 1
                if window[str2[window_start]] == 0:
                    window.pop(str2[window_start])
                window_start += 1
        
        return False
