class Processor:
    def __init__(self):
        self.outputs = []

    def add(self, output):
        self.outputs.append(output)

    def exec(self, imgs):  # FIXME: Does not work like that! Need dependency order
        res = []
        for img in imgs:
            for output in self.outputs:
                res.extend(output.exec([img]))
        return res
