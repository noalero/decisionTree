import dataPath


class Breed(object):
    def __init__(self, name, datapath_) -> None:
        self.__set_name__(name)
        self.__set_datapath__(datapath_)

    def __set_name__(self, name) -> None:
        self.name = name

    def get_name(self) -> str:
        return self.name

    def __set_datapath__(self, datapath_) -> None:
        self.datapath = datapath_

    def get_datapath(self) -> dataPath.DataPath:
        return self.datapath
