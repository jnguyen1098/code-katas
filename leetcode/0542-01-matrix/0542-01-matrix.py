class Solution:
    def updateMatrix(self, mat: List[List[int]]) -> List[List[int]]:
        
        INDETERMINATE = 99999
        rows = len(mat)
        cols = len(mat[0])
        incomplete = set()
        
        def matrix_complete(mat):
            return len(incomplete) == 0
        
        MOVES = (
                     (-1, 0),
            (0, -1),           (0, 1), 
                      (1, 0),
        ) 
        
        solution = []
        for i in range(len(mat)):
            solution.append([INDETERMINATE] * len(mat[0]))
            
            
        for i in range(len(mat)):
            for j in range(len(mat[0])):
                incomplete.add((i, j))
        
        locations = defaultdict(set)
        
        for i in range(len(mat)):
            for j in range(len(mat[i])):
                if mat[i][j] == 0:
                    solution[i][j] = 0
                    incomplete.discard((i, j))
                    locations[0].add((i, j))
        
        to_increment = 0
        while not matrix_complete(solution):
            to_move = []
            for i, j in locations[to_increment]:
                for dx, dy in MOVES:
                    x = i + dx
                    y = j + dy
                    if (x >= 0 and x < rows) and (y >= 0 and y < cols) and solution[x][y] == INDETERMINATE:
                        solution[x][y] = to_increment + 1
                        incomplete.discard((x, y))
                        to_move.append((x, y))
            for x, y in to_move:
                locations[to_increment].discard((x, y))
                locations[to_increment + 1].add((x, y))
            to_increment += 1
        
        return solution
