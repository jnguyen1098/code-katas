class Solution:
    def isValid(self, s: str) -> bool:
        
        stack = []
        
        def peek():
            if len(stack) == 0:
                return None
            return stack[-1]
        
        for char in s:
            
            if char == "a":
                stack.append("a")
                
            elif char == "b":
                if peek() != "a":
                    return False
                stack.append("b")
            
            elif char == "c":
                if peek() != "b":
                    return False
                stack.pop()
                if len(stack) == 0:
                    return False
                stack.pop()
        
        return len(stack) == 0
