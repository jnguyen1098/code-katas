class Solution:
    def findRoot(self, tree: List['Node']) -> 'Node':
        from_nodes = set()
        to_nodes = set()
        for thing in tree:
            from_nodes.add(thing)
            for child in thing.children:
                to_nodes.add(child)
        return from_nodes.difference(to_nodes).pop()
