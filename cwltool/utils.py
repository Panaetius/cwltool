# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import

# no imports from cwltool allowed

from six.moves import zip_longest
from typing import Any, Dict, List, Tuple, Text, Union


def aslist(l):  # type: (Any) -> List[Any]
    if isinstance(l, list):
        return l
    else:
        return [l]


def get_feature(self, feature):  # type: (Any, Any) -> Tuple[Any, bool]
    for t in reversed(self.requirements):
        if t["class"] == feature:
            return (t, True)
    for t in reversed(self.hints):
        if t["class"] == feature:
            return (t, False)
    return (None, None)

# comparision function to be used in sorting
# python3 doesn't allow sorting of different
# types like str() and int().
# this function re-creates sorting nature in py2
# of heterogeneous list of `int` and `str`
def cmp_like_py2(dict1, dict2):  # type: (Dict[Text, Any], Dict[Text, Any]) -> int
    # extract lists from both dicts
    a = dict1["position"]; b = dict2["position"]
    # iterate through both list till max of their size
    for i,j in zip_longest(a,b):
        if i == j:
            continue
        # in case 1st list is smaller
        # should come first in sorting
        if i is None:
            return -1
        # if 1st list is longer,
        # it should come later in sort
        elif j is None:
            return 1

        # if either of the list contains str element
        # at any index, both should be str before comparing
        if isinstance(i, str) or isinstance(j, str):
            return 1 if str(i) > str(j) else -1
        # int comparison otherwise
        return 1 if i > j else -1

    # if both lists are equal
    return 0

# util function to convert any present byte string
# to unicode string. input is a dict of nested dicts and lists
def bytes2str_in_dicts(a):
	# type: (Union[Dict[Text, Any], List[Any], Any]) -> Dict[Text, Any]

    # if input is dict, recursively call for each value
    if isinstance(a, dict):
        for k, v in dict.items(a):
            a[k] = bytes2str_in_dicts(v)

        return a

    # if list, iterate through list and fn call
    # for all its elements
    if isinstance(a, list):
        for idx, value in enumerate(a):
            a[idx] = bytes2str_in_dicts(value)

            return a
    # if value is bytes, return decoded string,
    elif isinstance(a, bytes):
        return a.decode('utf-8')

    # simply return elements itself
    else:
        return a