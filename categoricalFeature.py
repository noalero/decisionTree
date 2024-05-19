import feature


class CategoricalFeature(feature.Feature):

    def __init__(self, name: str, n_breeds: int, serial_number: int) -> None:
        super().__init__(name, n_breeds, serial_number)
        # self.__set_breeds__()

    def accept(self, visitor) -> None:  # visitor pattern
        visitor.visit_categorical_set_breeds(self)


