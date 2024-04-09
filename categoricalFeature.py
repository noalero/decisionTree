import feature


class CategoricalFeature(feature.Feature):

    def __init__(self, name, index, values) -> None:
        feature.Feature.__init__(self, name, index, values)
        self.__set_breeds__(values)

    def __set_breeds__(self, values) -> None:  # visitor pattern
        breeds = []
        pass

    def is_value_of_breed(self, breed_, value) -> bool:  # visitor pattern
        return breed_ == value
