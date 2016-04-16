import xml.dom.minidom
from PIL import ImageColor

from .output_node import OutputNode

from .nodes.add_node import AddNode
from .nodes.blur_node import BlurNode
from .nodes.mirror_node import MirrorNode
from .nodes.rotate_node import RotateNode
from .nodes.scale_node import ScaleNode
from .nodes.tint_node import TintNode

from ..exceptions import *
from ..modes import *


class Parser:
    def __init__(self, file):
        DOMTree = xml.dom.minidom.parse(file)
        self.root = DOMTree.documentElement

    def parse(self, processor):
        if self.root.tagName != 'package':
            raise XMLError("No root 'package' element found.")

        for input in self.root.getElementsByTagName('input'):
            if not input.hasAttribute('filter') and not input.hasAttribute('from'):
                raise XMLError('input node has no required "filter" or "from" attribute.')

            if input.hasAttribute('filter') and input.hasAttribute('from'):
                raise XMLError('input node has both "filter" and "from" attribute, but only one is allowed.')

            for output in input.getElementsByTagName('output'):
                output_node = OutputNode(input_filter=input.getAttribute('filter'),
                                         from_node=input.getAttribute('from'),
                                         label=
                                         output.getAttribute('label') if output.hasAttribute('label') else None,
                                         input_label=
                                         input.getAttribute('label') if input.hasAttribute('label') else None,
                                         package_label=
                                         self.root.getAttribute('label') if self.root.hasAttribute('label') else None,
                                         suppress=Parser.parse_boolean(output.getAttribute('suppress')))

                nodes = output.childNodes

                for node in nodes:
                    if node.nodeType != xml.dom.Node.ELEMENT_NODE:
                        continue

                    if node.tagName == 'tint':
                        node_node = TintNode(Parser.parse_color(node.getAttribute('color')),
                                             Parser.parse_filter_mode(node.getAttribute('mode')),
                                             max(0, min(1, float(node.getAttribute('opacity')))) if
                                             node.hasAttribute('opacity') else 1)
                        output_node.add(node_node)
                    elif node.tagName == 'scale':
                        if not node.hasAttribute('factor'):
                            raise XMLError("scale node has no required 'factor' attribute.")

                        x_scale, y_scale = Parser.parse_scale_factor(node.getAttribute('factor'))
                        node_node = ScaleNode(x_scale, y_scale,
                                              Parser.parse_resampling_mode(node.getAttribute('quality')))
                        output_node.add(node_node)
                    elif node.tagName == 'rotate':
                        node_node = RotateNode(float(node.getAttribute('degree')),
                                               Parser.parse_resampling_mode(node.getAttribute('quality')))
                        output_node.add(node_node)
                    elif node.tagName == 'mirror':
                        horz, vert = Parser.parse_mirror_dir(node.getAttribute('direction'))
                        node_node = MirrorNode(horz, vert)
                        output_node.add(node_node)
                    elif node.tagName == 'blur':
                        node_node = BlurNode(
                            max(0, float(node.getAttribute('strength'))) if node.hasAttribute('strength') else 1)
                        output_node.add(node_node)
                    elif node.tagName == 'add':
                        node_node = AddNode(node.getAttribute('input'),
                                            Parser.parse_input_type(node.getAttribute('input_type')),
                                            Parser.parse_filter_mode(node.getAttribute('mode')),
                                            max(0, min(1, float(node.getAttribute('opacity')))) if
                                            node.hasAttribute('opacity') else 1,
                                            Parser.parse_scale_mode(node.getAttribute('scale')))
                        output_node.add(node_node)
                    else:
                        raise XMLError("Unknown processing node '{}'".format(node.tagName))

                processor.add(output_node)

    @staticmethod
    def parse_boolean(str):
        if str == '1' or str.lower() == 'true' or str.lower() == 'on':
            return True
        else:
            return False

    @staticmethod
    def parse_color(str):
        if (len(str) != 4 and len(str) != 7) or str[0] != '#':
            raise XMLError('Color attribute is not valid.')

        return ImageColor.getrgb(str)

    @staticmethod
    def parse_filter_mode(str):
        if (not str) or str.lower() == 'normal':
            return ImageFilterMode.Normal
        elif str.lower() == 'multiply' or str.lower() == 'mul':
            return ImageFilterMode.Multiply
        elif str.lower() == 'add':
            return ImageFilterMode.Add
        elif str.lower() == 'subtract' or str.lower() == 'sub':
            return ImageFilterMode.Sub
        else:
            raise XMLError('Mode attribute is not valid.')

    @staticmethod
    def parse_mirror_dir(str):
        if (not str) or str.lower() == 'horz' or str.lower() == 'horizontal':
            return True, False
        elif str.lower() == 'vert' or str.lower() == 'vertical':
            return False, True
        elif str.lower() == 'both':
            return True, True
        else:
            raise XMLError('Direction attribute is not valid.')

    @staticmethod
    def parse_resampling_mode(str):
        if (not str) or str.lower() == 'nearest' or str.lower() == 'near':
            return ResamplingMode.Nearest
        elif str.lower() == 'bilinear':
            return ResamplingMode.Bilinear
        elif str.lower() == 'bicubic':
            return ResamplingMode.Bicubic
        else:
            raise XMLError('Quality attribute is not valid.')

    @staticmethod
    def parse_scale_factor(str):
        v = list(map(lambda x: float(x), str.split(',')))
        if len(v) == 1:
            return v[0], v[0]
        elif len(v) == 2:
            return v[0], v[1]
        else:
            raise XMLError('Factor attribute is not valid.')

    @staticmethod
    def parse_input_type(str):
        if (not str) or str.lower() == 'file':
            return InputTypeMode.File
        elif str.lower() == 'node':
            return InputTypeMode.Node
        else:
            raise XMLError('input_type attribute is not valid.')

    @staticmethod
    def parse_scale_mode(str):
        if (not str) or str.lower() == 'extend':
            return AddScaleMode.Extend
        elif str.lower() == 'min':
            return AddScaleMode.Min
        elif str.lower() == 'clamp':
            return AddScaleMode.Clamp
        else:
            raise XMLError('scale attribute for "add" node is not valid.')
