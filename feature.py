import string
# import numpy as np


class Feature(object):
    def __init__(self, name, values, n_breeds) -> None:
        self.__set_name__(name)
        # self.__set_breeds__(values,n_breeds)

    def __set_name__(self, name) -> None:
        self.name = name

    def get_name(self) -> string:
        return self.name

    def __set_breeds__(self, values, n_breeds) -> None:  # visitor pattern
        pass

    @staticmethod
    def get_breeds() -> list:
        # ToDo
        return []  # self.breeds

    def is_value_of_breed(self, breed, value) -> bool:  # visitor pattern
        pass
