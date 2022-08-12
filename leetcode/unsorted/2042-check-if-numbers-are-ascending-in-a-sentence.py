class Solution:
    def areNumbersAscending(self, s: str) -> bool:
        
        def is_ascending(numbers):
            for i in range(1, len(numbers)):
                if numbers[i] <= numbers[i - 1]:
                    return False
            return True
        
        numbers = [int(token) for token in s.split() if token.isnumeric()]
        return is_ascending(numbers)
