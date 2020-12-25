class Solution:
    def uniqueMorseRepresentations(self, words: List[str]) -> int:

        morse = [
            ".-","-...","-.-.","-..",".","..-.","--.","....","..",".---","-.-",
            ".-..","--","-.","---",".--.","--.-",".-.","...","-","..-","...-",
            ".--","-..-","-.--","--.."
        ]
        
        return len(set(["".join([morse[ord(char) - ord("a")] for char in word]) for word in words]))
