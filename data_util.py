import numpy as np


def smooth_data(l, width):
    length = len(l)
    target = [np.mean(l[max(0, i - width): min(i + width + 1, length)]) for i in range(length)]
    return target


def params_match(big, small):
    for k in small:
        if big[k] != small[k]:
            return False
    return True


def dict_list_to_df(dict_list, keys, constant_values_appended=None):
    """
    Returns [l_1, l_2, l_3, ..., l_n] where n = |keys| + |constant_values_appended|
    """
    all_arrays = [dict_list[k] for k in keys]
    if constant_values_appended is not None:
        all_arrays += [[c for _ in dict_list[keys[0]]] for c in constant_values_appended]
    return list(zip(*all_arrays))

def dict_to_kv_lists(d):
    return d
