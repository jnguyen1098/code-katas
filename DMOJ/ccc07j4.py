from collections import Counter

line1 = [char for char in input() if char != " "]
line2 = [char for char in input() if char != " "]

print("Is an anagram." if Counter(line1) == Counter(line2) else "Is not an anagram.")

