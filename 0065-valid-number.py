class Solution:
    def isNumber(self, s: str) -> bool:
        return re.match(r'^(\+|-)?((\d+\.\d+)|(\d+\.)|(\.\d+)|(\d+))([Ee][-+]?\d+)?$', s)
