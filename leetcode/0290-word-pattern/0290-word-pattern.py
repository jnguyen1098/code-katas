class Solution:
    def wordPattern(self, pattern: str, str: str) -> bool:
        words = str.split()
        if len(words) != len(pattern):
            return False
        rules = {}
        for i in range(len(pattern)):
            if pattern[i] in rules:
                if rules[pattern[i]] != words[i]:
                    return False
            elif words[i] in rules.values():
                    return False
            else:
                rules[pattern[i]] = words[i]
        return True
