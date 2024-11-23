class ETLBase:
    def extract(self):
        raise NotImplementedError("Extract method not implemented.")

    def transform(self, data):
        raise NotImplementedError("Transform method not implemented.")

    def load(self, data):
        raise NotImplementedError("Load method not implemented.")
