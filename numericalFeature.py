import feature
import range


class NumericalFeature(feature.Feature):
    def __init__(self, name, index, values) -> None:
        feature.Feature.__init__(self, name, index, values)
        self.__set_breeds__(values)

    def __set_breeds__(self, values) -> None:  # visitor pattern
        pass

    def is_value_of_breed(self, range_, value) -> bool:  # visitor pattern
        ans = True
        if value < range_.get_from_index() | value > range_.get_to_index():
            ans = False
        if not (range_.get_edges()[0]) & value == range_.get_from_index():
            ans = False
        if not (range_.get_edges()[1]) & value == range_.get_to_index():
            ans = False
        return ans
