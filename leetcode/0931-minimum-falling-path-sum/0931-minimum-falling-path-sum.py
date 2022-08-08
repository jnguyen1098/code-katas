class Solution:
    def minFallingPathSum(self, matrix: List[List[int]]) -> int:
        rows = len(matrix)
        cols = len(matrix[0])
        
        def fallthrough(x, y):
            MOVES = ((1, -1), (1, 0), (1, 1))
            options = []
            for dx, dy in MOVES:
                new_x = x + dx
                new_y = y + dy
                if (new_x >= 0 and new_x < rows) and (new_y >= 0 and new_y < cols):
                    options.append((new_x, new_y))
            return options
        
        for i in reversed(range(rows - 1)):
            for j in range(cols):
                incr = math.inf
                for x, y in fallthrough(i, j):
                    incr = min(incr, matrix[x][y])
                matrix[i][j] += incr
        
        
        min_path = math.inf
        for i in range(cols):
            min_path = min(min_path, matrix[0][i])
            
        return min_path
