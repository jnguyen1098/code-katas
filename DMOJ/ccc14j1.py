a1 = int(input())
a2 = int(input())
a3 = int(input())

totalSum = a1 + a2 + a3
lengthSet = set([a1, a2, a3])

print(a1, a2, a3)

if totalSum != 180:
    print("Error")
elif len(lengthSet) == 1:
    print("Equilateral")
elif len(lengthSet) == 2:
    print("Isosceles")
else:
    print("Scalene")
