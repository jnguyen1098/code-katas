class Solution:
    def findClosestElements(self, arr: List[int], k: int, x: int) -> List[int]:
        sorted_elems = sorted(arr, key=lambda y: abs(x - y))
        result = []
        for i in range(k):
            result.append(sorted_elems[i])
        return sorted(result)
