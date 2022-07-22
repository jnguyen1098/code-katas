class Solution:
    def diagonalSum(self, mat: List[List[int]]) -> int:
        nums = set()
        
        rows = len(mat)
        cols = len(mat[0])
        
        x, y = 0, 0
        while x < rows and y < cols:
            nums.add((x, y))
            x += 1
            y += 1
        
        x, y = 0, cols - 1
        while x < rows and y < cols:
            nums.add((x, y))
            x += 1
            y -= 1
        
        result = 0
        
        for x, y in nums:
            result += mat[x][y]
        
        return result
