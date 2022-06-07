
def chunks_array(l, n):
    n = max(1, n)
    return (l[i:i+n] for i in range(0, len(l), n))

def array_normalize(arr, t_min, t_max):
    norm_arr = []
    diff = t_max - t_min
    diff_arr = max(arr) - min(arr)
    for i in arr:
        temp = (((i - min(arr))*diff)/diff_arr) + t_min
        norm_arr.append(temp)
    return norm_arr

def dict_normalize(importances):
    norm_dict = dict()
    min_imp = min(importances.values())
    max_imp = max(importances.values())
    for key, val in importances.items():
        norm_dict[key] = value_normalize(val, min_imp, max_imp)
    return norm_dict

def value_normalize(val, min_val, max_val):
    return (val - min_val) / (max_val - min_val)

def normalize_value_range(val, min_val, max_val, min_range, max_range):
    return (max_range - min_range) * ((val - min_val) / (max_val - min_val)) + min_range