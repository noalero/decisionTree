import feature
import numericalFeature
import categoricalFeature
import breed
import leaf
import parent


class DataPath(object):
    def __init__(self) -> None:
        pass

    def __set_size__(self, size) -> None:
        self.size = size

    def get_size(self) -> int:
        return self.size

    def __set_path__(self, path) -> None:
        self.path = path
        pass

    def get_path(self) -> list:
        return self.path

    def add_feature(self, feature_) -> None:
        pass
        # resize

    def add_breed(self, breed_) -> None:
        pass  # resize
