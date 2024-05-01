class Feature(object):
    def __init__(self, name: str, n_breeds: int) -> None:
        self.__set_name__(name)
        self.__set_n_breeds__(n_breeds)
        # self.__set_breeds__(values,n_breeds)

    def __set_name__(self, name) -> None:
        self.name = name

    def __set_n_breeds__(self, n_breeds) -> None:
        self.n_breeds = n_breeds

    def __set_breeds__(self, values: list, n_breeds: int) -> None:  # visitor pattern
        # TODO
        pass

    def get_name(self) -> str:
        return self.name

    def get_n_breeds(self) -> int:
        return self.n_breeds

    @staticmethod
    def get_breeds(self) -> list:
        return self.breeds

