# this took me 7 submits to AC I want to die

class Solution:
    def placeWordInCrossword(self, board: List[List[str]], word: str) -> bool:
        
        rows = len(board)
        cols = len(board[0])
        
        def valid(x, y, char):
            return (0 <= x < rows) and (0 <= y < cols) and board[x][y] in [" ", char]
        
        def go_up(x, y, frag):
            if len(frag) == 1 and board[x][y] in [" ", frag] and (x == 0 or board[x - 1][y] == "#"):
                return True
            if x > 0 and len(frag) > 0 and board[x][y] in [" ", frag[0]]:
                return go_up(x - 1, y, frag[1:])
            return False
        
        def go_down(x, y, frag):
            if len(frag) == 1 and board[x][y] in [" ", frag] and (x == rows - 1 or board[x + 1][y] == "#"):
                return True
            if x < rows and len(frag) > 0 and board[x][y] in [" ", frag[0]]:
                return go_down(x + 1, y, frag[1:])
            return False
        
        def go_left(x, y, frag):
            if len(frag) == 1 and board[x][y] in [" ", frag] and (y == 0 or board[x][y - 1] == "#"):
                return True
            if y > 0 and len(frag) > 0 and board[x][y] in [" ", frag[0]]:
                return go_left(x, y - 1, frag[1:])
            return False
        
        def go_right(x, y, frag):
            if len(frag) == 1 and board[x][y] in [" ", frag] and (y == cols - 1 or board[x][y + 1] == "#"):
                return True
            if y < cols and len(frag) > 0 and board[x][y] in [" ", frag[0]]:
                return go_right(x, y + 1, frag[1:])
            return False
        
        n = set()
        
        for i in range(cols):
            if board[0][i] in [" ", word[0], word[-1]]:
                n.add((0, i))
                
        s = set()
        for i in range(cols):
            if board[rows - 1][i] in [" ", word[0], word[-1]]:
                s.add((rows - 1, i))
                
        w = set()
        for i in range(rows):
            if board[i][0] in [" ", word[0], word[-1]]:
                w.add((i, 0))
                
        e = set()
        for i in range(rows):
            if board[i][cols - 1] in [" ", word[0], word[-1]]:
                e.add((i, cols - 1))
                
        for i in range(rows):
            for j in range(cols):
                if board[i][j] == "#":
                    if valid(i - 1, j, word[-1]) or valid(i - 1, j, word[0]):
                        s.add((i - 1, j))
                    if valid(i + 1, j, word[0]) or valid(i + 1, j, word[-1]):
                        n.add((i + 1, j))
                    if valid(i, j - 1, word[-1]) or valid(i, j - 1, word[0]):
                        e.add((i, j - 1))
                    if valid(i, j + 1, word[0]) or valid(i, j + 1, word[-1]):
                        w.add((i, j + 1))
        
        for x, y in n:
            try:
                if go_down(x, y, word):
                    return True
            except:
                continue
        
        for x, y in s:
            try:
                if go_up(x, y, word):
                    return True
            except:
                continue
        
        for x, y in w:
            try:
                if go_right(x, y, word):
                    return True
            except:
                continue
        
        for x, y in e:
            try:
                if go_left(x, y, word):
                    return True
            except:
                continue
        
        return False
