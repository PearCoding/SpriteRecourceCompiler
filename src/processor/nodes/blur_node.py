from ..processing_node import ProcessingNode
from PIL import ImageFilter


class BlurNode(ProcessingNode):
    def __init__(self, strength):
        self.strength = strength

    def exec(self, processor, img):
        return [img.filter(ImageFilter.GaussianBlur(self.strength))]
