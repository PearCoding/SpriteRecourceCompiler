from processor.processing_node import ProcessingNode
from PIL import Image


class MirrorNode(ProcessingNode):
    def __init__(self, horz, vert):
        self.horz = horz
        self.vert = vert

    def exec(self, imgs):
        res = []
        for img in imgs:
            tmp = img
            if self.horz:
                tmp = tmp.transpose(Image.FLIP_TOP_BOTTOM)
            if self.vert:
                tmp = tmp.transpose(Image.FLIP_LEFT_RIGHT)
            res.append(tmp)
        return res
