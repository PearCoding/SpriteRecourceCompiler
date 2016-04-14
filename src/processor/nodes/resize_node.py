from processor.processing_node import ProcessingNode


class ResizeNode(ProcessingNode):
    def __init__(self, width, height, quality):
        self.width = width
        self.height = height
        self.quality = quality

    def exec(self, img):
        return [img.resize((self.width, self.height), self.quality.toPIL())]
