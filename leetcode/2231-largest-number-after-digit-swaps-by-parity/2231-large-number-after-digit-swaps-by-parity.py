class Solution:
    def largestInteger(self, num: int) -> int:
        
        odds = []
        evens = []
        
        message_queue = []
        for char in str(num):
            if int(char) % 2 == 0:
                message_queue.append("Even")
                evens.append(int(char))
            else:
                message_queue.append("Odd")
                odds.append(int(char))
                
        odds.sort()
        evens.sort()
                
        result = []
        
        for message in message_queue:
            if message == "Even":
                result.append(str(evens.pop()))
            elif message == "Odd":
                result.append(str(odds.pop()))
        
        return int("".join(result))
                
