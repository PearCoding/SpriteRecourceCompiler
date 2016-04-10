import xml.dom.minidom
from processor.package_node import PackageNode
from processor.input_node import InputNode
from processor.output_node import OutputNode


class XMLError(Exception):
    def __init__(self, str):
        self.str = str

    def __str__(self):
        return 'XML Error: {}'.format(self.str)


class Parser:
    def __init__(self, file):
        DOMTree = xml.dom.minidom.parse(file)
        self.root = DOMTree.documentElement

    def parse(self, processor):
        if self.root.tagName != 'package':
            raise XMLError("No root 'package' element found.")

        package_node = PackageNode(processor)
        inputs = self.root.getElementsByTagName('input')
        for input in inputs:
            if not input.hasAttribute('filter'):
                raise XMLError('input node has no required filter attribute.')

            input_node = InputNode(processor, input.getAttribute('filter'),
                                   input.getAttribute('label') if input.hasAttribute('label') else None)

            outputs = input.getElementsByTagName('output')
            for output in outputs:
                # from_attr = output.getAttribute('from')

                output_node = OutputNode(input_node,
                                         input.getAttribute('label') if input.hasAttribute('label') else None,
                                         input.getAttribute('suppress') if input.hasAttribute('suppress') else None)

                nodes = output.childNodes

                for node in nodes:
                    proc_node = None
                    if node.tagName == 'tint':
                        pass
                    elif node.tagName == 'scale':
                        pass
                    elif node.tagName == 'rotate':
                        pass
                    elif node.tagName == 'mirror':
                        pass
                    elif node.tagName == 'blur':
                        pass
                    elif node.tagName == 'add':
                        pass
                    else:
                        raise XMLError("Unknown processing node '{}'".format(node.tagName))

                    output_node.add(proc_node)

                input_node.add(output_node)

            package_node.add(input_node)

        processor.add(package_node)