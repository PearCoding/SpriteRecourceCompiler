class PackageNode:
    def __init__(self, processor, label=None):
        self.processor = processor
        self.label = label
        self.inputs = []
        self.production = []

    def add(self, input):
        self.inputs.append(input)

    def exec(self, path):
        res = []
        for input in self.inputs:
            res.extend(input.exec(path))

        return res
