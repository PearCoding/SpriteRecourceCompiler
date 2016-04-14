from processor.processing_node import ProcessingNode
from PIL import Image


class RotateNode(ProcessingNode):
    def __init__(self, degree, quality):
        self.degree = degree
        self.quality = quality

    def exec(self, processor, img):
        if self.degree == 360:
            return [img]

        if self.degree == 90:
            return [img.transpose(Image.ROTATE_90)]
        elif self.degree == 180:
            return [img.transpose(Image.ROTATE_180)]
        elif self.degree == 270:
            return [img.transpose(Image.ROTATE_270)]
        else:
            return [img.rotate(self.degree, self.quality.toPIL(), True)]
