class ProcessingNode:
    def exec(self, processor, img):
        raise NotImplementedError()

    def dependencies(self, processor):
        return []
