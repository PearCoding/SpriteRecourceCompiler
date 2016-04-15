from PIL import Image
from processor.processing_node import ProcessingNode
from modes import ImageFilterMode


class TintNode(ProcessingNode):
    def __init__(self, color, mode, opacity):
        self.color = color
        self.mode = mode
        self.opacity = opacity

    def exec(self, processor, img):
        R, G, B = 0, 1, 2

        source = img.split()

        if self.mode == ImageFilterMode.Multiply:
            r = source[R].point(lambda i: i * (1-self.opacity) + (self.color[R]/255)*i*self.opacity)
            g = source[G].point(lambda i: i * (1-self.opacity) + (self.color[G]/255)*i*self.opacity)
            b = source[B].point(lambda i: i * (1-self.opacity) + (self.color[B]/255)*i*self.opacity)
        elif self.mode == ImageFilterMode.Add:
            r = source[R].point(lambda i: i * (1 - self.opacity) + min(255, self.color[R] + i) * self.opacity)
            g = source[G].point(lambda i: i * (1 - self.opacity) + min(255, self.color[G] + i) * self.opacity)
            b = source[B].point(lambda i: i * (1 - self.opacity) + min(255, self.color[B] + i) * self.opacity)
        elif self.mode == ImageFilterMode.Sub:
            r = source[R].point(lambda i: i * (1 - self.opacity) + max(0, self.color[R] + i) * self.opacity)
            g = source[G].point(lambda i: i * (1 - self.opacity) + max(0, self.color[G] + i) * self.opacity)
            b = source[B].point(lambda i: i * (1 - self.opacity) + max(0, self.color[B] + i) * self.opacity)
        else:  # ImageFilterMode.Normal:
            r = source[R].point(lambda i: i * (1 - self.opacity) + self.color[R] * self.opacity)
            g = source[G].point(lambda i: i * (1 - self.opacity) + self.color[G] * self.opacity)
            b = source[B].point(lambda i: i * (1 - self.opacity) + self.color[B] * self.opacity)

        source[R].paste(r)
        source[G].paste(g)
        source[B].paste(b)

        return [Image.merge(img.mode, source)]
