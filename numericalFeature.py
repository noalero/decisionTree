import feature


class NumericalFeature(feature.Feature):
    def __init__(self, name: str, values: list[float], n_breeds: int, serial_number: int) -> None:
        feature.Feature.__init__(self, name, n_breeds, serial_number)
        # self.__set_breeds__()


    def get_min_max_vals(self, rows) -> tuple[float, float]:
        min_val = max_val = rows[0][0]
        for row in rows:
            if row[0] > max_val:
                max_val = row[0]
            elif row[0] < min_val:
                min_val = row[0]
        return min_val, max_val

    def accept(self, visitor) -> None:  # visitor pattern
        visitor.visit_numerical_set_breeds(self)


