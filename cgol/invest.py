from collections import Counter

arrays = []

num_slices = 8
num_people = 4

array = [0] * num_people

def recursively_build_array(position_to_increment, array_length):
    if position_to_increment == array_length:
        arrays.append((sum(array), array[:]))
        return
    for number in range(1, num_slices + 1):
        array[position_to_increment] = number
        recursively_build_array(position_to_increment + 1, array_length)

recursively_build_array(0, num_people)

arrays.sort()

counter = Counter([item[0] for item in arrays])

for i in range(4, 32 + 1):
    print(i, counter[i])

def is_nondecreasing(arr):
    for i in range(1, len(arr)):
        if arr[i] < arr[i - 1]:
            return False
    return True

non_dec_count = 0

for arr_sum, array in arrays:
    if is_nondecreasing(array):
        non_dec_count += 1

print(non_dec_count)
