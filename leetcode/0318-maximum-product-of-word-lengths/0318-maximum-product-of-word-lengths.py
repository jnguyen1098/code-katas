class Solution:
    def maxProduct(self, words: List[str]) -> int:
        masks = []
        for word in words:
            masks.append((len(word), set(word)))
        prod = 0
        
        for i in range(len(masks)):
            for j in range(i, len(masks)):
                if len(masks[i][1] & masks[j][1]) > 0:
                    continue
                prod = max(prod, masks[i][0] * masks[j][0])
        
        return prod
