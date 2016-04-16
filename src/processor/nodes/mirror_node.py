from ..processing_node import ProcessingNode
from PIL import Image


class MirrorNode(ProcessingNode):
    def __init__(self, horz, vert):
        self.horz = horz
        self.vert = vert

    def exec(self, processor, img):
        if self.horz:
            return [img.transpose(Image.FLIP_TOP_BOTTOM)]
        if self.vert:
            return [img.transpose(Image.FLIP_LEFT_RIGHT)]
