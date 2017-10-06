
def multiply_dict_by_constant(dct,constant):
    for key in sorted(dct):
        if type(dct[key]) is dict:
            multiply_dict_by_constant(dct[key],constant)
        else:
            dct[key] *= constant

def format_dict_as_strings(dct,formatStr):
    for key in sorted(dct):
        if type(dct[key]) is dict:
            format_dict_as_strings(dct[key],formatStr)
        else:
            dct[key] = formatStr % dct[key]