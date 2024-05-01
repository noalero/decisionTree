import numpy as np


def __calc_entropy__(self, total, *args, **kwargs) -> float:
    if len(args) == 1 and isinstance(args[0], list) and not kwargs:
        return self.__calc_entropy_list__(total, args[0])
    elif 'pos' in kwargs and 'neg' in kwargs and len(kwargs) == 2 and not args:
        return self.__calc_entropy_bin__(total, kwargs['pos'], kwargs['neg'])
    else:
        raise ValueError("Invalid argument combination")


def __calc_entropy_bin__(self, total, pos: int, neg: int) -> float:
    pos_p = self.__calc_p__(total, pos)
    neg_p = self.__calc_p__(total, neg)
    log_pos_p = np.log(pos_p)
    log_neg_p = np.log(neg_p)
    entropy = (pos_p * log_pos_p + neg_p * log_neg_p) * (-1.)
    return entropy


def __calc_entropy_list__(self, total, classes: list[int]) -> float:
    mult_sum = 0.
    for cls in classes:
        p = self.__calc_p__(total, cls)
        log_p = np.log(p)
        p_log_p = p * log_p
        mult_sum += p_log_p
    entropy = mult_sum * (-1.)
    return entropy


# calc_p:
@staticmethod
def __calc_p__(total, some) -> float:
    return some / total


# e_parent_feature:
def e_parent_feature(self, breeds_: list[tuple]) -> float:
    # ToDo
    first_tuple = breeds_[0]
    if isinstance(first_tuple[1], list):
        func_call = self.__calc_entropy__(first_tuple[0], first_tuple[1])
    elif isinstance(first_tuple[1], int) and len(first_tuple) == 3 and isinstance(first_tuple[2], int):
        func_call = self.__calc_entropy__(first_tuple[0], pos=first_tuple[1], neg=first_tuple[2])
    else:
        raise TypeError("Unexpected tuple structure in breeds_ list")
    expectations: list[float] = []
    total_sum = 0  # (0.?)
    for breed_ in breeds_:
        exp = func_call
        total = breed_[0]
        expectations.append(exp * total)
        total_sum += total
    e_parent = 0.
    for exp in expectations:
        e_parent += exp
    e_parent = e_parent / total_sum
    return e_parent


# calc_information_gain:
def __calc_information_gain__(self, breeds, total) -> float:
    # ToDo
    # From [feature_] get it's list of breeds [feature_.breeds]
    # From [datapath_] get pos, neg, total for each breed and create [breeds_] list
    pos = 0.0
    neg = 0.0
    entropy = self.__calc_entropy__(total, pos, neg)
    return 0.0

