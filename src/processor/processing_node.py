class ProcessingNode:
    def execute(self, processor, img):
        raise NotImplementedError()

    def dependencies(self, processor):
        return []
