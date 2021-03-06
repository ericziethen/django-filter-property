
import os

from django.db import connection
from django_filters import FilterSet


# https://stackoverflow.com/questions/34439/finding-what-methods-a-python-object-has
def get_function_dic_for_class(obj, ignore):
    # Some functions are unique for all classes
    ignore_funcs = ['__init_subclass__', '__subclasshook__']

    return {name: getattr(obj, name) for name in dir(obj)
            if callable(getattr(obj, name)) and name not in ignore_funcs and
            (ignore is None or name not in ignore)}


def class_functions_diff_dic(class1, class2, *, ignore=None):
    diff_dic = {}

    funcs1 = get_function_dic_for_class(class1, ignore)
    funcs2 = get_function_dic_for_class(class2, ignore)
    combined_names = set(list(funcs1.keys()) + list(funcs2.keys()))

    in1_not2 = []
    in2_not1 = []
    different_sig = []

    for name in combined_names:
        if name in funcs1 and name in funcs2:
            if funcs1[name] != funcs2[name]:
                different_sig.append((name, funcs1[name], funcs2[name]))
        else:
            if name in funcs1:
                in1_not2.append(name)
            else:
                in2_not1.append(name)

    if in1_not2:
        diff_dic[F'In {class1.__name__} not in {class2.__name__}'] = sorted(in1_not2)

    if in2_not1:
        diff_dic[F'In {class2.__name__} not in {class1.__name__}'] = sorted(in2_not1)

    if different_sig:
        diff_dic['Different Address'] = sorted(different_sig)

    return diff_dic


def db_is_sqlite():
    return connection.vendor == 'sqlite'


def db_is_postgresql():
    return connection.vendor == 'postgresql'


def is_ci_build():
    return 'IS_CI_BUILD' in os.environ


def all_filter_volume_test_enabled():
    return 'ALL_FILTER_VOLUME_TEST' in os.environ
