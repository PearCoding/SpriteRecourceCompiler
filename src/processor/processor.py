class Processor:
    def __init__(self):
        self.packages = []

    def add(self, package):
        self.packages.append(package)

    def exec(self, imgs):  # FIXME: Does not work like that! Need dependency order
        res = []
        for img in imgs:
            for package in self.packages:
                res.extend(package.exec(img))
        return res
