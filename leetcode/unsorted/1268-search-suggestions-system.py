class Trie:
    def __init__(self):
        self.data = {}

    def insert(self, word: str) -> None:
        tracer = self.data
        for char in word:
            if char not in tracer:
                tracer[char] = {}
            tracer = tracer[char]
        tracer["*"] = True

    def search(self, word: str) -> bool:
        tracer = self.data
        for char in word:
            if char not in tracer:
                return False
            tracer = tracer[char]
        return "*" in tracer

class Solution:
    def suggestedProducts(self, products: List[str], searchWord: str) -> List[List[str]]:
        
        memory = []
        
        def traverse(data, curr_word=[]):
            if data is None:
                return
            if isinstance(data, bool) or len(data.keys()) == 0:
                memory.append("".join(curr_word))
                return
            for char, trie in data.items():
                if char != "*":
                    curr_word.append(char)
                traverse(trie)
                if char != "*":
                    curr_word.pop()
                    
        def get_node(data, prefix):
            tracer = data
            for char in prefix:
                if char not in tracer:
                    return None
                tracer = tracer[char]
            return tracer
        
        trie = Trie()
        
        for product in products:
            trie.insert(product)
        
        suggestions = []
        
        for i in range(len(searchWord)):
            query = searchWord[:i + 1]
            node = get_node(trie.data, query)
            traverse(node)
            memory = [f"{query}{item}" for item in memory]
            memory.sort()
            tmp = []
            for i in range(3):
                if i >= len(memory):
                    break
                tmp.append(memory[i])
            suggestions.append(tmp)
            memory.clear()
        
        return suggestions
