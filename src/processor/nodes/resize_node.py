from ..processing_node import ProcessingNode


class ResizeNode(ProcessingNode):
    def __init__(self, width, height, quality):
        self.width = int(width)
        self.height = int(height)
        self.quality = quality

    def execute(self, processor, img):
        return [img.resize((self.width, self.height), self.quality.to_pil())]
