from typing import  Optional

from feature import Feature
from breed import Breed


class DataPath(object):
    def __init__(self, size, orgnl_path: list[tuple[Feature, Breed]],
                 new_dir: Optional[tuple[Feature, Breed]] = ()) -> None:
        self.__set_size__(size)
        if new_dir:
            self.__set_path__(orgnl_path, new_dir)
        else:
            self.path = orgnl_path

    def __set_size__(self, size) -> None:
        self.size = size

    def __set_path__(self, orgnl_path: list[tuple[Feature, Breed]],
                     new_dir: tuple[Feature, Breed]) -> None:
        self.path = orgnl_path.append(new_dir)
        self.__set_size__(self.size + 1)

    def get_size(self) -> int:
        return self.size

    def get_path(self) -> list[tuple[Feature, Breed]]:
        return self.path

    def get_f_type(self) -> str:
        # TODO: test
        f_type = ""
        for dir_ in self.path:
            f_type += str(dir_[0].get_serial_number())
        return f_type

    def get_f_val(self) -> str:
        # TODO: test
        f_type = ""
        for dir_ in self.path:
            f_type += str(dir_[1].get_serial_number())
        return f_type

