import fnmatch
import os
from PIL import Image


class OutputNode:
    def __init__(self, input_filter, label=None, input_label=None, package_label=None, suppress=False, from_node=None):
        self.label = label
        self.input_label = input_label
        self.package_label = package_label
        self.input_filter = input_filter
        self.suppress = suppress
        self.from_node = from_node
        self.nodes = []

        # Processing tmps
        self.production = []
        self.dependencies = set()  # General ones
        self.from_dependencies = set()

    def add(self, node):
        self.nodes.append(node)

    def exec(self, processor, imgs):
        res = []
        for img in imgs:
            if self.from_node or fnmatch.fnmatchcase(os.path.basename(img), self.input_filter):
                if self.from_node:
                    tmp = [img]
                else:
                    tmp = [Image.open(img)]
                for node in self.nodes:
                    new_tmp = []
                    for o in tmp:
                        new_tmp.extend(node.exec(processor, o))
                    tmp = new_tmp
                res.extend(tmp)
        self.production = res
        if self.suppress:
            return []
        else:
            return res