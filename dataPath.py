import feature
import brange
from typing import Union


class DataPath(object):
    def __init__(self, size, orgnl_path: list[tuple[feature.Feature, brange.Range | str]],
                 new_dir: tuple[feature.Feature, brange.Range | str]) -> None:
        self.__set_size__(size)
        self.__set_path__(orgnl_path, new_dir)

    def __set_size__(self, size) -> None:
        self.size = size

    def __set_path__(self, orgnl_path: list[tuple[feature.Feature, brange.Range | str]],
                     new_dir: tuple[feature.Feature, brange.Range | str]) -> None:
        self.path = orgnl_path.append(new_dir)
        self.__set_size__(self.size + 1)

    def get_size(self) -> int:
        return self.size

    def get_path(self) -> list:
        return self.path


