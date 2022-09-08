class Solution:
    def countWords(self, words1: List[str], words2: List[str]) -> int:
        
        def distinct(words):
            result = set()
            counter = {}
            
            for word in words:
                if word not in counter:
                    counter[word] = 0
                counter[word] += 1
                
            for word, freq in counter.items():
                if freq == 1:
                    result.add(word)
            
            return result
        
        return len(distinct(words1).intersection(distinct(words2)))
