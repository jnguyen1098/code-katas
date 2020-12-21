def next_n(n):
    result = 0
    while n > 0:
        result += (n % 10) ** 2
        n //= 10
    return result

class Solution:
    def isHappy(self, n: int) -> bool:
        
        fast = n
        slow = n
        
        while True:
            fast = next_n(next_n(fast))
            slow = next_n(slow)
            if fast == slow:
                return fast == 1
