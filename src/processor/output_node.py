class OutputNode:
    def __init__(self, input_node, label=None, suppress=False, from_node=None):
        self.label = label
        self.suppress = suppress
        self.input_node = input_node
        self.from_node = from_node
        self.nodes = []
        self.production = []

    def add(self, node):
        self.nodes.append(node)

    def exec(self, path):
        # TODO: Add processing!
        pass