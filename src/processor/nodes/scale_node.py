from ..processing_node import ProcessingNode


class ScaleNode(ProcessingNode):
    def __init__(self, x_scale, y_scale, quality):
        self.x_scale = x_scale
        self.y_scale = y_scale
        self.quality = quality

    def execute(self, processor, img):
        return [img.resize((int(img.width*self.x_scale), int(img.height*self.y_scale)), self.quality.toPIL())]
