command_list = []


class Command:
    def __init__(self):
        self.__keys = []
        self.description = ""
        self.file = False
        self.get_content = False
        self.return_content = False
        command_list.append(self)

    @property
    def keys(self):
        return self.__keys

    @keys.setter
    def keys(self, mas):
        for k in mas:
            self.__keys.append(k.lower())

    def process(self):
        pass
