class Solution:
    def selfDividingNumbers(self, left: int, right: int) -> List[int]:
        result = []
        for i in range(left, right + 1):
            fail = False
            dummy = i
            while dummy != 0:
                if dummy % 10 == 0:
                    fail = True
                    break
                if (i % (dummy % 10)) != 0:
                    fail = True
                    break
                dummy = dummy // 10
            if fail != True:
                result.append(i)
        return result
