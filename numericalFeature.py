import config
import feature
import brange
import tree_data_bases as tdb


class NumericalFeature(feature.Feature):
    def __init__(self, name: str, values: list[float], n_breeds: int, serial_number: int) -> None:
        feature.Feature.__init__(self, name, n_breeds, serial_number)
        self.__set_breeds__()


    def __get_min_max_vals(self, rows) -> tuple[float, float]:
        min_val = max_val = rows[0][0]
        for row in rows:
            if row[0] > max_val:
                max_val = row[0]
            elif row[0] < min_val:
                min_val = row[0]
        return min_val, max_val

    def __set_breeds__(self) -> None:  # visitor pattern
        # TODO: test
        if self.n_breeds == 0:
            raise ZeroDivisionError("calc_p: Total is zero")
        self.breeds = set()
        column = self.name
        rows = tdb.select_table([column], [], config.training_t_name)
        min_val, max_val = self.__get_min_max_vals(rows)
        brange_size = (max_val - min_val) / abs(self.n_breeds)  # if n_breeds < 0: default value
        if brange_size == 0:
            self.breeds.add(min_val)
        else:
            lft = min_val
            rght = min_val + brange_size
            for i in range(self.n_breeds):
                self.breeds.add(brange.Range(lft, rght))
                lft = rght
                rght = lft + brange_size

