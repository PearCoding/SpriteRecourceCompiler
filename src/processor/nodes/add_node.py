from processor.processing_node import ProcessingNode
from modes import *

import fnmatch


class AddNode(ProcessingNode):
    def __init__(self, input, type, mode, opacity, size):
        self.input = input
        self.type = type
        self.mode = mode
        self.opacity = opacity
        self.size_mode = size

    def exec(self, processor, img):
        imgs = []
        if self.type == InputTypeMode.File:
            for file in processor.files:
                if fnmatch.fnmatchcase(file, self.input):
                    imgs.append(Image.open(file))
        else:
            for node in processor.get_nodes(self.input):
                imgs.extend(node.production)

        if len(imgs) == 0:
            return [img]
        else:
            res = []

            return res

    def dependencies(self, processor):
        if self.type == InputTypeMode.File:
            return []
        else:
            return processor.get_nodes(self.input)
