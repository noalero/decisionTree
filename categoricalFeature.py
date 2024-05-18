import config
import feature
import tree_data_bases as tdb


class CategoricalFeature(feature.Feature):

    def __init__(self, name: str, n_breeds: int, serial_number: int) -> None:
        feature.Feature.__init__(self, name, n_breeds, serial_number)
        self.__set_breeds__()

    def __set_breeds__(self) -> None:  # visitor pattern
        # TODO: test
        self.breeds = set()
        breed_count = self.n_breeds  # if there is no limitation to the number of breeds, n_breeds < 0
        column = self.name
        rows = tdb.select_table([column], [], config.training_t_name)
        for row in rows:
            if breed_count == 0:
                break
            self.breeds.add(row[0])
            breed_count = breed_count - 1

