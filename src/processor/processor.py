from ..exceptions import *


class Processor:
    def __init__(self):
        self.outputs = []
        self.files = []

    def add(self, output):
        self.outputs.append(output)

    def get_nodes(self, str):
        res = []
        parts = str.split(',')
        for part in parts:
            entry = part.split('.')
            if len(entry) > 3:
                raise ProcessorError('Too much label parts given "."')

            if len(entry) == 3:
                ret = self.search_node(entry)
            elif len(entry) == 2:
                ret = self.search_node([None, entry[0], entry[1]])
            elif len(entry) == 1:
                ret = self.search_node([None, None, entry[0]])
            else:
                raise ProcessorError('Internal error.')

            if not len(ret):
                raise ProcessorError(
                    'No outputs from label "{0}"'.format(part))
            res.extend(ret)

        return res

    def search_node(self, labels):
        res = []
        for output in self.outputs:
            if (labels[2] == '*' or output.label == labels[2]) and\
                    (labels[1] == '*' or output.input_label == labels[1]) and\
                    (labels[0] == '*' or output.package_label == labels[0]):
                res.append(output)

        return res

    def setup_dependencies(self):
        # Build dependencies.
        for output in self.outputs:
            if output.from_node:
                nodes = self.get_nodes(output.from_node)
                output.dependencies.update(nodes)
                output.from_dependencies.update(nodes)

            for node in output.nodes:
                output.dependencies.update(node.dependencies(self))

    def exec_rec(self, output, imgs, stack):
        if output in stack:
            raise ProcessorError(
                'Cyclic dependency in processing graph found.')

        if output.production:
            return output.production
        else:
            stack.append(output)
            if output.from_node:
                res = []
                for dependency in output.from_dependencies:
                    res.extend(self.exec_rec(dependency, imgs, stack))
                ret = output.execute(self, res)
            else:
                ret = output.execute(self, imgs)
            stack.pop()
            return ret

    def execute(self, imgs):
        self.files = imgs
        self.setup_dependencies()

        stack = []
        for output in self.outputs:
            self.exec_rec(output, imgs, stack)

        res = []
        for output in self.outputs:
            if not output.suppress:
                name = output.label if output.label else "_unknown_"
                if len(output.production) == 1:
                    res.append(type('processor_output', (object,),
                                    {"name": name,
                                     "file": output.production[0]}))
                else:
                    counter = 1
                    for prod in output.production:
                        res.append(type('processor_output', (object,),
                                        {"name": "%s_%i" % (name, counter),
                                         "file": prod}))
                        counter += 1

        return res
