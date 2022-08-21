import math

def get_prime_count(num):
    count = 0
    last_range = num + 1
    last = num
    orig = num
    prime = False
    while num > 1:
        for fac in range(2, last_range):
            if fac == orig:
                prime = True
            if num % fac == 0:
                count += 1
                num //= fac
                break
        if last == num:
            break
        else:
            last = num
    print(count if not prime else 0)

for _ in range(5):
    get_prime_count(int(input()))
