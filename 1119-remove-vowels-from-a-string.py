class Solution:
    def removeVowels(self, s: str) -> str:
        result = ""
        
        for char in s:
            if char not in "aeiou":
                result += char
        
        return result
    
"""
class Solution:
    def removeVowels(self, s: str) -> str:
        return "".join(c for c in s if c not in "aeiou")
"""
