from processor.processing_node import ProcessingNode


class TintNode(ProcessingNode):
    def __init__(self, color, mode, opacity):
        self.color = color
        self.mode = mode
        self.opacity = opacity

    def exec(self, img):
        pass
