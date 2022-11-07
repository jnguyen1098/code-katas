class Solution:
    def toGoatLatin(self, sentence: str) -> str:
        
        def begins_with_vowel(word):
            return word[0] in "AEIOUaeiou"
        
        def begins_with_consonant(word):
            return not begins_with_vowel(word)
        
        def convert(word, idx):
            if begins_with_vowel(word):
                word += "ma"
            elif begins_with_consonant(word):
                word = word[1:] + word[0] + "ma"
            else:
                raise Exception("Word neither starts with defined consonant or vowel...")
            return word + ("a" * (idx + 1))
        
        result = []
        
        for idx, word in enumerate(sentence.split()):
            result.append(convert(word, idx))
        
        return " ".join(result)
