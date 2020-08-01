class Solution:
    def detectCapitalUse(self, word: str) -> bool:
        return re.match(r"\b([A-Z]+|[A-Z][a-z]+|[a-z]+)\b", word)
