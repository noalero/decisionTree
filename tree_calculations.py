import numpy as np
import math

def calc_total(sums: list[int]) -> int:
    total: int = 0
    print("total:")
    for s in sums:
        total += s
        print("t = ", total)
    return total


def calc_entropy(*args, **kwargs) -> float:
    if len(args) == 1 and isinstance(args[0], list) and not kwargs:
        return calc_entropy_list(args[0])
    elif 'pos' in kwargs and 'neg' in kwargs and len(kwargs) == 2 and not args:
        return calc_entropy_bin(kwargs['pos'], kwargs['neg'])
    else:
        raise ValueError("Invalid argument combination")


def calc_entropy_bin(pos: int, neg: int) -> float:
    total = calc_total([pos, neg])
    pos_p = calc_p(total, pos)
    neg_p = calc_p(total, neg)
    log_pos_p = np.log(pos_p)
    log_neg_p = np.log(neg_p)
    entropy = (pos_p * log_pos_p + neg_p * log_neg_p) * (-1.)
    return entropy


def calc_entropy_list(total: int, classes_amounts: list[int]) -> float:
    # total = calc_total(classes_amounts)
    mult_sum = 0.
    for cls in classes_amounts:
        try:
            p = calc_p(total, cls)
        except ZeroDivisionError as e:
            print(e)
        else:
            log_p = np.log(p)
            p_log_p = p * log_p
            mult_sum += p_log_p
    entropy = mult_sum * (-1.)
    print("entropy = ", entropy)
    return entropy


def calc_p(total:int, some:int) -> float:
    if total == 0:
        raise ZeroDivisionError("calc_p: Total is zero")
    return some / total


def e_parent_feature(breeds_: list[list[int]]) -> float:
    # first_tuple = breeds_[0]  # <total, list: classes> || <total, pos, neg>
    # if isinstance(first_tuple[1], list):
    #     func_call = calc_entropy(first_tuple[1])
    # elif isinstance(first_tuple[1], int) and len(first_tuple) == 3 and isinstance(first_tuple[2], int):
    #     func_call = calc_entropy(pos=first_tuple[1], neg=first_tuple[2])
    # else:
    #     raise TypeError("Unexpected tuple structure in breeds_ list")
    totals = []
    e_parent = 0.
    for breed_ in breeds_:
        total = calc_total(breed_)
        exp = calc_entropy_list(total, breed_)
        e_parent += exp * total
        totals.append(total)
    total_sum = calc_total(totals)
    e_parent = e_parent / total_sum
    print("e_parent = ", e_parent)
    return e_parent


# calc_information_gain:
def calc_information_gain(breeds: list[list[int]], parent_classes: list[int]) -> float:
    # ToDo
    # From [feature_] get it's list of breeds [feature_.breeds]
    # From [datapath_] get pos, neg, total for each breed and create [breeds_] list
    e_parent_feat = e_parent_feature(breeds)
    total_p = calc_total(parent_classes)
    e_parent = calc_entropy_list(total_p, parent_classes)
    information_gain = e_parent - e_parent_feat
    return information_gain

