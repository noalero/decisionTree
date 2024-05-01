import feature
import numericalFeature
import categoricalFeature
import breed
import leaf
import parent
import decisionTree


class DataPath(object):
    def __init__(self, size, orgnl_path: list[tuple[feature.Feature, breed.Breed]], new_dir: tuple[feature.Feature, breed.Breed]) -> None:
        self.__set_size__(size)
        self.__set_path__(orgnl_path, new_dir)

# getters & setters of class attributes:
    # size:
    def __set_size__(self, size) -> None:
        self.size = size

    def get_size(self) -> int:
        return self.size

    # path
    def __set_path__(self, orgnl_path: list[tuple[feature.Feature, breed.Breed]], new_dir: tuple[feature.Feature, breed.Breed]) -> None:
        self.path = orgnl_path.append(new_dir)
        self.__set_size__(self.size + 1)

    def get_path(self) -> list:
        return self.path


