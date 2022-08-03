class Solution:
    def getKth(self, lo: int, hi: int, k: int) -> int:
        
        def get_power(num, cache={1: 0}):
            if num in cache:
                return cache[num]
            if num % 2 == 0:
                next_num = num // 2
            else:
                next_num = 3 * num + 1
            cache[num] = get_power(next_num) + 1
            return cache[num]
        
        nums = list(range(lo, hi + 1))
        
        return sorted(nums, key=get_power)[k - 1]
