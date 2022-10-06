class Solution:
    def kthDistinct(self, arr: List[str], k: int) -> str:
        counter = {}
        for word in arr:
            if (deref := counter.get(word)) is None:
                counter[word] = 0
            counter[word] += 1
        
        distincts = []
        for word, freq in counter.items():
            if freq == 1:
                distincts.append(word)
            
        return distincts[k - 1] if len(distincts) > k - 1 else ""
