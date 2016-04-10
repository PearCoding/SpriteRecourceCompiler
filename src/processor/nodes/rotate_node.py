from processor.processing_node import ProcessingNode
from PIL import Image


class RotateNode(ProcessingNode):
    def __init__(self, degree, quality):
        self.degree = degree
        self.quality = quality

    def exec(self, imgs):
        if self.degree == 360:
            return imgs

        res = []
        for img in imgs:
            tmp = img
            if self.degree == 90:
                tmp = tmp.transpose(Image.ROTATE_90)
            elif self.degree == 180:
                tmp = tmp.transpose(Image.ROTATE_180)
            elif self.degree == 270:
                tmp = tmp.transpose(Image.ROTATE_270)
            else:
                tmp = tmp.rotate(self.degree, self.quality.toPIL(), True)
            res.append(tmp)
        return res
