import os
import fnmatch
from PIL import Image


class InputNode:
    def __init__(self, package_node, filter, label=None):
        self.package_node = package_node
        self.filter = filter
        self.label = label
        self.outputs = []
        self.production = []

    def add(self, output):
        self.outputs.append(output)

    def exec(self, path):
        if fnmatch.fnmatchcase(os.path.basename(path), self.filter):
            image = Image.open(path)
            # TODO: Add processing!