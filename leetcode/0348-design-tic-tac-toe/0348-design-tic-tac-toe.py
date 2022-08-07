class TicTacToe:

    def __init__(self, n: int):
        self.board = []
        for _ in range(n):
            tmp = []
            for __ in range(n):
                tmp.append("")
            self.board.append(tmp)
        self.record = {
            "X": {
                "row": defaultdict(set),
                "column": defaultdict(set),
                "diagonal": defaultdict(set),
            },
            "O": {
                "row": defaultdict(set),
                "column": defaultdict(set),
                "diagonal": defaultdict(set),
            },
        }
        self.l_diag = set()
        x, y = 0, 0
        while x < len(self.board) and y < len(self.board):
            self.l_diag.add((x, y))
            x += 1
            y += 1
        self.r_diag = set()
        x, y = 0, len(self.board) - 1
        while x < len(self.board) and y >= 0:
            self.r_diag.add((x, y))
            x += 1
            y -= 1
        
    def get_winner(self):
        for player in ["X", "O"]:
            for disposition in ["row", "column", "diagonal"]:
                for idx, members in self.record[player][disposition].items():
                    if len(members) == len(self.board):
                        return 1 if player == "X" else 2
        return None

    def move(self, row: int, col: int, player: int) -> int:
        char = "X" if player == 1 else "O"
        self.board[row][col] = char
        self.record[char]["row"][row].add((row, col))
        self.record[char]["column"][col].add((row, col))
        if (row, col) in self.l_diag: self.record[char]["diagonal"][1].add((row, col))
        if (row, col) in self.r_diag: self.record[char]["diagonal"][2].add((row, col))
        if (winner := self.get_winner()) is not None:
            return winner
        return 0
