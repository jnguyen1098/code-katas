class Solution:
    def anagramMappings(self, A: List[int], B: List[int]) -> List[int]:
        indexes = {}
        
        for idx, val in enumerate(B):
            indexes[val] = idx
        
        return [indexes[val] for val in A]
