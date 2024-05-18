import config
import feature
import brange


class NumericalFeature(feature.Feature):
    def __init__(self, name: str, values: list[float], n_breeds: int, serial_number: int) -> None:
        feature.Feature.__init__(self, name, n_breeds, serial_number)
        self.__set_breeds__(values, n_breeds)

    def __set_breeds__(self, values: list[float], n_breeds: int) -> None:  # visitor pattern
        self.breeds = set()
        min_val = min(values)
        max_val = max(values)
        brange_size = (max_val - min_val) / abs(n_breeds)  # if n_breeds < 0: default value
        edges = (True, False)
        for i in range(abs(n_breeds) - 1):
            self.breeds.add(brange.Range(min_val, max_val, edges))
            min_val = max_val
            max_val = max_val + brange_size
        self.breeds.add(brange.Range(min_val, max_val, (True, True)))

    # def is_value_of_breed(self, brange_, value) -> bool:  # visitor pattern
    #     ans = True
    #     if value < brange_.get_from_index() | value > brange_.get_to_index():
    #         ans = False
    #     if not (brange_.get_edges()[0]) & value == brange_.get_from_index():
    #         ans = False
    #     if not (brange_.get_edges()[1]) & value == brange_.get_to_index():
    #         ans = False
    #     return ans
