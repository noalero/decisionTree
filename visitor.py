from abc import ABC, abstractmethod

import categoricalFeature
import feature
import numericalFeature
from brange import Range
import config
import tree_data_bases as tdb


class FeatureVisitor(ABC):
    @abstractmethod
    def visit_numerical_set_breeds(self, feature_name: str) -> None:
        pass

    @abstractmethod
    def visit_categorical_set_breeds(self, feature_name: str) -> None:
        pass


class ConcreteFeatureVisitor(FeatureVisitor):
    def visit_numerical_set_breeds(self, feature_n: numericalFeature.NumericalFeature) -> None:
        # TODO: test
        if feature_n.get_n_breeds() == 0:
            raise ZeroDivisionError("calc_p: Total is zero")
        feature_n.breeds = set()
        column = feature_n.get_name()
        rows = tdb.select_table([column], [], config.training_t_name)
        min_val, max_val = feature_n.get_min_max_vals(rows)
        brange_size = (max_val - min_val) / abs(feature_n.get_n_breeds())  # if n_breeds < 0: default value
        if brange_size == 0:
            feature_n.breeds.add(min_val)
        else:
            lft = min_val
            rght = min_val + brange_size
            for i in range(feature_n.n_breeds):
                feature_n.breeds.add(Range(lft, rght))
                lft = rght
                rght = lft + brange_size

    def visit_categorical_set_breeds(self, feature_c: categoricalFeature.CategoricalFeature) -> None:
        # TODO: test
        feature_c.breeds = set()
        breed_count = feature_c.get_n_breeds()  # if there is no limitation to the number of breeds, n_breeds < 0
        column = feature_c.get_name()
        rows = tdb.select_table([column], [], config.training_t_name)
        for row in rows:
            if breed_count == 0:
                break
            feature_c.breeds.add(row[0])
            breed_count = breed_count - 1

