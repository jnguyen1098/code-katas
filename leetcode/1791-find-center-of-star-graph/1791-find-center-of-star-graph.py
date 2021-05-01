class Solution:
    def findCenter(self, edges: List[List[int]]) -> int:
        return (set(edges[0]) & set(edges[1])).pop()
