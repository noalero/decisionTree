import numpy as np
import sqlalchemy as sa

from brange import Range
from dataPath import DataPath
from feature import Feature
import tree_data_bases as tdb
from breed import Breed


def calc_total(sums: list[int]) -> int:
    total: int = 0
    for s in sums:
        total += s
    print("total: ", total)
    return total


# def calc_entropy(*args, **kwargs) -> float:
#     if len(args) == 1 and isinstance(args[0], list) and not kwargs:
#         return calc_entropy_list(args[0])
#     elif 'pos' in kwargs and 'neg' in kwargs and len(kwargs) == 2 and not args:
#         return calc_entropy_bin(kwargs['pos'], kwargs['neg'])
#     else:
#         raise ValueError("Invalid argument combination")


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
    mult_sum = 0.0
    for cls in classes_amounts:
        if cls == 0:
            continue
        try:
            p = calc_p(total, cls)
        except ZeroDivisionError as e:
            print(e)
        else:
            log_p = np.log2(p)
            p_log_p = p * log_p
            mult_sum -= p_log_p
    entropy = mult_sum  # * (-1.0)
    print("entropy = ", entropy)
    return entropy


def calc_p(total: int, some: int) -> float:
    if total == 0:
        raise ZeroDivisionError("calc_p: Total is zero")
    ans = some / total
    return ans


def e_parent_feature(breeds_: list[list[int]]) -> float:
    totals = []
    e_parent = 0.0
    for breed_ in breeds_:
        total = calc_total(breed_)
        exp = calc_entropy_list(total, breed_)
        e_parent += exp * total
        totals.append(total)
    total_sum = calc_total(totals)
    e_parent = e_parent / total_sum
    print("e_parent = ", e_parent)
    return e_parent


def calc_information_gain(breeds: list[list[int]], parent_classes: list[int]) -> float:
    e_parent_feat = e_parent_feature(breeds)
    total_p = calc_total(parent_classes)
    e_parent = calc_entropy_list(total_p, parent_classes)
    information_gain = e_parent - e_parent_feat
    return information_gain


def calc_feature_breeds_amount(feat: Feature, dp: DataPath, classes: list[str]) -> list[list[int]]:
    # TODO: test
    breeds: set[Breed] = feat.get_breeds()
    breeds_amounts: list[list[int]] = []
    for brd in breeds:
        new_dir = (feat, brd)
        new_dp = DataPath(dp.get_size(), dp.path, new_dir)
        amount = tdb.get_path_classes_amounts(new_dp, classes)
        breeds_amounts.append(amount)
    return breeds_amounts


def calc_feature_entropy(feat: Feature, dp: DataPath, classes: list[str]) -> float:
    # TODO: test
    breeds_amounts: list[list[int]] = calc_feature_breeds_amount(feat, dp, classes)
    feat_breed_entropy = e_parent_feature(breeds_amounts)
    return feat_breed_entropy


def calc_feature_information_gain(feat: Feature, dp: DataPath, classes: list[str]) -> float:
    # TODO: test
    breeds_amounts: list[list[int]] = calc_feature_breeds_amount(feat, dp, classes)
    parent_classes: list[int] = tdb.get_path_classes_amounts(dp, classes)
    inf_gain = calc_information_gain(breeds_amounts, parent_classes)
    return inf_gain
