class Solution:
    def maxRepeating(self, sequence: str, word: str) -> int:
        if word not in sequence:
            return 0
        i = 0
        while True:
            sub = ""
            for j in range(i):
                sub += word
            if len(sub) <= len(sequence):
                if sub not in sequence:
                    break
            else:
                break
            i += 1
        return i - 1
