import string
import numpy as np
class Feature(object):

    def __init__(self, name, index, values) -> None
        self.__set_name__(name)
        self.__set_index__(index)
        self.__set_breeds__(values)

    def __set_name__(self, name) -> None:
        self.name = name

    def get_name(self) -> string:
        return self.name

    def __set_index__(self, index) -> None:
        self.index = index

    def get_index(self) -> int:
        return self.index

    def __set_breeds__(self, values) -> None: # visitor pattern
        pass

    def get_breeds(self) -> list:
        return self.breeds

    def is_value_of_breed(self, breed, value) -> bool: # visitor pattern
        pass

