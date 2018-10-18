class ConfigDoesNotExist(Exception):
    def __init__(self, path):
        self.path = path

    def __repr__(self, ):
        return f"ConfigDoesNotExist({self.path})"
