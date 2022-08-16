class Solution:
    def equalSubstring(self, s: str, t: str, maxCost: int) -> int:
        
        # note len(s) == len(t)
        
        maxlen = 0
        curlen = 0
        curcost = 0
        
        l = 0
        for r in range(len(s)):
            l_char = s[r]
            r_char = t[r]
            cost = abs(ord(l_char) - ord(r_char))
            while curcost + cost > maxCost:
                curcost -= abs(ord(s[l]) - ord(t[l]))
                curlen -= 1
                l += 1
            else:
                curcost += cost
                curlen = r - l + 1
                maxlen = max(maxlen, curlen)
        
        return maxlen
