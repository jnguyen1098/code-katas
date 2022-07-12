class Solution:
    def decodeMessage(self, key: str, message: str) -> str:
        
        def make_unique_string(word):
            seen = set()
            result = []
            
            for char in word:
                if char in seen:
                    continue
                seen.add(char)
                result.append(char)
            
            return "".join(result)
        
        cleaned_key = "".join([char for char in make_unique_string(key) if char.isalpha()])

        mapping = str.maketrans(cleaned_key + " ", "abcdefghijklmnopqrstuvwxyz ")
        
        return message.translate(mapping)
