class Solution:
    def flipAndInvertImage(self, A: List[List[int]]) -> List[List[int]]:
        A = reversed(A)
        result = []
        for row in A:
            tmp_row = []
            for i in range(len(row) - 1, -1, -1):
                if row[i] == 0:
                    tmp_row.append(1)
                else:
                    tmp_row.append(0)
            result.append(tmp_row)
        return reversed(result)
