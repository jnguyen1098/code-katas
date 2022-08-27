from collections import Counter 

N = int(input())

nums = [int(num) for num in input().split()]

assert N == len(nums)

def get_mean():
    if len(nums) == 0:
        raise Exception("bruh")
    return sum(nums) / len(nums)

def get_median():
    if len(nums) == 1:
        return nums[0]
    if len(nums) == 2:
        return (nums[0] + nums[1]) / 2
    sorted_nums = sorted(nums)
    if len(sorted_nums) % 2 == 1:
        return sorted_nums[len(sorted_nums) // 2]
    return (sorted_nums[len(sorted_nums) // 2] + sorted_nums[len(sorted_nums) // 2 - 1]) / 2

def get_modes():
    modes = []
    counter = Counter(nums)
    highest_count = max(counter.values())
    for key, value in counter.items():
        if value == highest_count:
            modes.append(str(key))
    return sorted(modes)

print(get_mean())
print(get_median())
print(" ".join(get_modes()))
