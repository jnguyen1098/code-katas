class Solution:
    def totalFruit(self, tree: List[int]) -> int:
        
        freqs = {}
        window_start = 0
        answer = 0
        
        for window_end in range(len(tree)):
            
            right_char = tree[window_end]
            if right_char not in freqs:
                freqs[right_char] = 0
            freqs[right_char] += 1

            while len(freqs) > 2:
                left_char = tree[window_start]
                freqs[left_char] -= 1
                if freqs[left_char] == 0:
                    freqs.pop(left_char)
                window_start += 1
            
            answer = max(answer, window_end - window_start + 1)
        
        return answer
