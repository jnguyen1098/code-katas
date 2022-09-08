class Solution:
    def countVowelSubstrings(self, word: str) -> int:
        
        count = 0
        
        for i in range(len(word)):
            for j in range(i, len(word)):
                counter = defaultdict(int)
                for k in range(i, j + 1):
                    counter[word[k]] += 1
                if len(counter.keys()) == 5 and set(counter.keys()) == set(["a", "e", "i", "o", "u"]):
                    count += 1
        
        return count:

