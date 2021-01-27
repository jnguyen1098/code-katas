class Solution:
    def isPalindrome(self, s: str) -> bool:
        rev = [char.lower() for char in s if char.isalnum()]
        return rev == list(reversed(rev))
