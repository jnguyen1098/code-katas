class Solution:
    def convertTime(self, current: str, correct: str) -> int:
        
        def get_absolute_minutes(timestring):
            hours, minutes = map(int, timestring.split(":"))
            return (hours * 60) + minutes
        
        cu_s = get_absolute_minutes(current)
        co_s = get_absolute_minutes(correct)
        
        ops = 0
        
        while cu_s != co_s:
            if cu_s + 60 <= co_s:
                cu_s += 60
                ops += 1
            elif cu_s + 15 <= co_s:
                cu_s += 15
                ops += 1
            elif cu_s + 5 <= co_s:
                cu_s += 5
                ops += 1
            else:
                cu_s += 1
                ops += 1
        
        return ops
