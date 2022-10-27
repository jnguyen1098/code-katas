# i cheated on this question and just submitted the output of this program xD

def get_divisors(num):
    divisors = []
    for i in range(1, num):
        if num % i == 0:
            divisors.append(i)
    return divisors

def perfect(num):
    divisors = get_divisors(num)
    if num == sum(divisors):
        return True
    return False

def get_digits(num):
    digits = []
    for char in str(num):
        digits.append(int(char))
    return digits

def cube_perfect(num):
    summation = 0
    for digit in get_digits(num):
        summation += digit ** 3
    return num == summation

for i in range(1000, 9999 + 1):
    if perfect(i):
        print(i)

for i in range(100, 999 + 1):
    if cube_perfect(i):
        print(i)
