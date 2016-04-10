from processor.processing_node import ProcessingNode


class BlurNode(ProcessingNode):
    def __init__(self, strength):
        self.strength = strength

    def exec(self, img):
        pass
