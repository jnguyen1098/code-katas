import copy
class Solution:
    def permuteUnique(self, s: List[int]) -> List[List[int]]:
        
        result = []
        s.sort()
        result.append(copy.deepcopy(s))
        
        while True:
            
            i = -1
            for it in range(0, len(s) - 1):
                if s[it] < s[it + 1]:
                    i = it
            
            if i == -1:
                break
                
            j = i + 1
            for it in range(i + 1, len(s)):
                if s[i] < s[it]:
                    j = it
            
            tmp_s = s[i]
            s[i] = s[j]
            s[j] = tmp_s
            
            rev = []
            for it in range(i + 1, len(s)):
                rev.append(s[it])
            
            rev.reverse()
            
            for it in range(i + 1, len(s)):
                s[it] = rev[it - (i + 1)]
                
            result.append(copy.deepcopy(s))
        
        return result
