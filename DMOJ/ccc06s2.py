class ParseMap(dict):
    def __missing__(self, key):
        return "."

plaintext = input()
ciphertext = input()
mystery = input()

print(mystery.translate(ParseMap({ord(y): x for x, y in zip(plaintext, ciphertext)})))
