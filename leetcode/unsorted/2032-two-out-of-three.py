class Solution:
    def twoOutOfThree(self, nums1: List[int], nums2: List[int], nums3: List[int]) -> List[int]:
        
        counter = defaultdict(int)
        
        for arr in [nums1, nums2, nums3]:
            for letter in set(arr):
                counter[letter] += 1
        
        result = []
        
        for number, freq in counter.items():
            if freq >= 2:
                result.append(number)
        
        return result
