from abc import ABC, abstractmethod

import categoricalFeature
import feature
import numericalFeature
from brange import Range
import config
import tree_data_bases as tdb
from breed import Breed


class FeatureVisitor(ABC):
    @abstractmethod
    def visit_set_breeds_numerical(self, feature_name: str) -> None:
        pass

    @abstractmethod
    def visit_set_breeds_categorical(self, feature_name: str) -> None:
        pass


class ConcreteFeatureVisitor(FeatureVisitor):
    def visit_set_breeds_numerical(self, feature_n: numericalFeature.NumericalFeature) -> None:
        # TODO: test
        if feature_n.get_n_breeds() == 0:
            raise ZeroDivisionError("calc_p: Total is zero")
        feature_n.breeds = set[Breed]()
        column = feature_n.get_name()
        rows = tdb.select_table([column], [], config.training_t_name)
        min_val, max_val = feature_n.get_min_max_vals(rows)
        brange_size = (max_val - min_val) / abs(feature_n.get_n_breeds())  # if n_breeds < 0: default value
        serial_number_count = 1
        if brange_size == 0:
            new_breed = Breed(Range(min_val, max_val), 1)
            feature_n.breeds.add(new_breed)
        else:
            lft = min_val
            rght = min_val + brange_size
            for i in range(feature_n.n_breeds):
                new_breed = Breed(Range(lft, rght), serial_number_count)
                feature_n.breeds.add(new_breed)
                serial_number_count += 1
                lft = rght
                rght = lft + brange_size

    def visit_set_breeds_categorical(self, feature_c: categoricalFeature.CategoricalFeature) -> None:
        # TODO: test
        feature_c.breeds = set[Breed]()
        breed_count = feature_c.get_n_breeds()  # if there is no limitation to the number of breeds, n_breeds < 0
        column = feature_c.get_name()
        rows = tdb.select_table([column], [], config.training_t_name)
        serial_number_count = 1
        for row in rows:
            if breed_count == 0:
                break
            new_breed = Breed(row[0], serial_number_count)
            feature_c.breeds.add(new_breed)
            serial_number_count += 1
            breed_count = breed_count - 1

