class Range:
    def __init__(self, from_index: float, to_index: float) -> None:
        self.__set_from_index__(from_index)
        self.__set_to_index__(to_index)
        # self.__set_edges__(edges[0], edges[1])

    def __set_from_index__(self, index) -> None:
        self.from_index = index

    def get_from_index(self) -> float:
        return self.from_index

    def __set_to_index__(self, index) -> None:
        self.to_index = index

    def get_to_index(self) -> float:
        return self.to_index

    # def __set_edges__(self, left, right) -> None:
    #     self.left_edge = left
    #     self.right_edge = right
    #
    # def get_edges(self) -> tuple:
    #     return self.left_edge, self.right_edge
