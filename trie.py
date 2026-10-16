class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root

        for char in word.lower():
            if char not in node.children:
                node.children[char] = TrieNode()

            node = node.children[char]

        node.is_end = True

    def _find_node(self, prefix):
        node = self.root

        for char in prefix.lower():
            if char not in node.children:
                return None

            node = node.children[char]

        return node

    def get_suggestions(self, prefix):
        node = self._find_node(prefix)

        if node is None:
            return []

        suggestions = []

        def dfs(current, path):
            if current.is_end:
                suggestions.append(prefix.lower() + path)

            for char, child in current.children.items():
                dfs(child, path + char)

        dfs(node, "")

        return suggestions