from processor.processing_node import ProcessingNode


class ScaleNode(ProcessingNode):
    def __init__(self, x_scale, y_scale, quality):
        self.x_scale = x_scale
        self.y_scale = y_scale
        self.quality = quality

    def exec(self, imgs):
        res = []
        for img in imgs:
            res.append(img.resize((img.width*self.x_scale, img.height*self.y_scale), self.quality.toPIL()))
        return res
