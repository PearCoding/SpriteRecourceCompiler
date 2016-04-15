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
            print("Warning: Empty production in 'add' node.")
            return [img]
        else:
            res = []
            for other in imgs:
                if self.size_mode == AddScaleMode.Extend:
                    width = max(img.width, other.width)
                    height = max(img.height, other.height)
                elif self.size_mode == AddScaleMode.Min:
                    width = min(img.width, other.width)
                    height = min(img.height, other.height)
                else:  # Clamp
                    width = img.width
                    height = img.height

                tmp = Image.new("RGBA", (width, height))

                tmp_a = tmp.load()
                img_a = img.load()
                other_a = other.load()

                R, G, B, A, = 0, 1, 2, 3

                for y in range(0, height):
                    for x in range(0, width):
                        color_img = img_a[x, y] if y < img.height and x < img.width else (0, 0, 0, 0)
                        color_oth = other_a[x, y] if y < other.height and x < other.width else (0, 0, 0, 0)

                        opacity = self.opacity * (color_oth[A]/255)
                        r = color_img[R] * (1-opacity)
                        g = color_img[G] * (1-opacity)
                        b = color_img[B] * (1-opacity)
                        a = color_img[A]

                        if self.mode == ImageFilterMode.Multiply:
                            r += (color_oth[R] / 255) * color_img[R] * opacity
                            g += (color_oth[G] / 255) * color_img[G] * opacity
                            b += (color_oth[B] / 255) * color_img[B] * opacity
                        if self.mode == ImageFilterMode.Add:
                            r += min(255, color_oth[R] + color_img[R]) * opacity
                            b += min(255, color_oth[G] + color_img[G]) * opacity
                            b += min(255, color_oth[B] + color_img[B]) * opacity
                        elif self.mode == ImageFilterMode.Sub:
                            r += max(0, color_oth[R] - color_img[R]) * opacity
                            g += max(0, color_oth[G] - color_img[G]) * opacity
                            b += max(0, color_oth[B] - color_img[B]) * opacity
                        elif self.mode == ImageFilterMode.Normal:
                            r += color_oth[R] * opacity
                            g += color_oth[G] * opacity
                            b += color_oth[B] * opacity

                        tmp_a[x, y] = (int(r), int(g), int(b), int(a))

                res.append(tmp)
        return res

    def dependencies(self, processor):
        if self.type == InputTypeMode.File:
            return []
        else:
            return processor.get_nodes(self.input)
