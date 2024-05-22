from brange import  Range


class Breed(object):
    def __init__(self, name: str | Range, serial_number: int) -> None:
        self.__set_name__(name)
        self.__set_serial_number__(serial_number)

    def __set_name__(self, name) -> None:
        self.name = name

    def __set_serial_number__(self, serial_num: int) -> None:
        self.serial_number = serial_num

    def get_name(self) -> str | Range:
        return self.name

    def get_serial_number(self) -> int:
        return self.serial_number
