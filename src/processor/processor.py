class ProcessorError(Exception):
    def __init__(self, str):
        self.str = str

    def __str__(self):
        return 'Processing Error: {}'.format(self.str)


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
                raise ProcessorError('No outputs from label "{}"'.format(part))
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

        # Check for cyclic dependencies.
        for output in self.outputs:
            if Processor.is_cyclic(output, []):
                raise ProcessorError('Cyclic dependency in processing graph found.')

    @staticmethod
    def is_cyclic(output, stack):
        for dependency in output.dependencies:
            if dependency in stack:
                return True

            stack.append(dependency)
            if not Processor.is_cyclic(dependency, stack):
                return True
        return False

    def exec_rec(self, output, imgs, stack):
        if output.from_node:
            res = []
            for dependency in output.from_dependencies:
                if dependency in stack:
                    res.extend(dependency.production)
                else:
                    stack.append(dependency)
                    res.extend(Processor.exec_rec(dependency, imgs, stack))
            return output.exec(self, res)
        else:
            return output.exec(self, imgs)

    def exec(self, imgs):
        self.files = imgs
        self.setup_dependencies()

        res = []
        stack = []
        for output in self.outputs:
            if output in stack:
                stack.append(output)
                res.extend(output.production)
            else:
                res.extend(self.exec_rec(output, imgs, stack))
        return res
