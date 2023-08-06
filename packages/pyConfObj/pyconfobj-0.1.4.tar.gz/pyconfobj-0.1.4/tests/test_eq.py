import pytest
from definitions import *


def test_conf_obj_eq():
    a0 = A()
    a0.atr_int = 3
    a0.atr_str = "Whatever"
    a1 = A()
    a1.atr_int = 3
    a1.atr_str = "Whatever"
    assert a0 == a1
    a2 = A()
    a2.atr_int = 4
    a2.atr_str = "Whatever"
    assert a2 != a0
    a2.atr_str = "whenever"
    assert a2 != a0
    assert a2 != 3
    assert a2 != 'whatever'


def test_conf_obj_list_eq():
    a0 = A()
    a0.atr_int = 3
    a0.atr_str = "Whatever"
    a1 = A()
    a1.atr_int = 2
    a1.atr_str = "Whenever"

    al0 = AList()
    al0.alist.append(a0)
    al0.alist.append(a1)
    al1 = AList()
    al1.alist.append(a0)
    al1.alist.append(a1)

    assert al0 == al1
    al1.alist.append(a1)
    assert al0 != al1








