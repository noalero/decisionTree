import feature


class CategoricalFeature(feature.Feature):

    def __init__(self, name, index, values, n_breeds) -> None:
        feature.Feature.__init__(self, name, index, values, n_breeds)
        self.__set_breeds__(values, n_breeds)

    def __set_breeds__(self, values, n_breeds) -> None:  # visitor pattern
        self.breeds = set()
        breed_count = n_breeds  # if there is no limitation to the number of breeds, n_breeds < 0
        for val in values:
            if breed_count == 0:
                break
            if not (val in self.breeds):
                self.breeds.add(val)
                breed_count = breed_count - 1

    def is_value_of_breed(self, breed_, value) -> bool:  # visitor pattern
        return breed_ == value
