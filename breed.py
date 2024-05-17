import dataPath


class Breed(object):
    def __init__(self, name: str, datapath_: dataPath.DataPath, serial_number: int) -> None:
        self.__set_name__(name)
        self.__set_datapath__(datapath_)
        self.__set_serial_number__(serial_number)

    def __set_name__(self, name) -> None:
        self.name = name

    def __set_datapath__(self, datapath_) -> None:
        self.datapath = datapath_

    def __set_serial_number__(self, serial_num: int) -> None:
        self.serial_number = serial_num

    def get_name(self) -> str:
        return self.name

    def get_datapath(self) -> dataPath.DataPath:
        return self.datapath

    def get_serial_number(self) -> int:
        return self.serial_number
