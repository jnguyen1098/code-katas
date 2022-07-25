N = int(input())

def convert(num: int) -> str:
    """Convert integer to binary, but as a string with groups of 4."""
    bitstring = bin(num)[2:]
    digits = len(bitstring) // 4 * 4 + (4 if len(bitstring) % 4 != 0 else 0)
    final_digits = []
    for char in reversed(bitstring):
        final_digits.append(char)
    for _ in range(digits - len(final_digits)):
        final_digits.append("0")
    output = []
    for idx, char in enumerate(final_digits):
        output.append(char)
        if (idx + 1) % 4 == 0:
            output.append(" ")
    return "".join(reversed(output)).removeprefix(" ")

for _ in range(N):
    print(convert(int(input())))
