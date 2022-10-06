shift = int(input())
line = input()

output = []

for char in line:
    if char == " ":
        new_char = " "
    elif char.isupper():
        new_char = chr((ord(char) - ord("A") - shift) % 26 + ord("A"))
    elif char.islower():
        new_char = chr((ord(char) - ord("a") - shift) % 26 + ord("a"))
    else:
        raise Exception("uh")
    output.append(new_char)

print("".join(output))
