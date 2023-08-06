from definitions import *


def test_confobj_yaml():
    a0 = A()
    a0.atr_int = 3
    a0.atr_str = "Whatever"
    b0 = B()
    b0.atr_a = a0
    b0.atr_int = 4
    b0.save_as_yaml('tmp.yaml')
    b1 = B()
    b1.load_yaml('tmp.yaml')
    assert b0 == b1


def test_confojlist_yaml():
    al0 = AList()
    a0 = A()
    a0.atr_int = 3
    a0.atr_str = "Whatever"
    a1 = A()
    a1.atr_int = 55
    a1.atr_str = "Whenever"
    al0.alist.append(a0)
    al0.alist.append(a1)
    al0.save_as_yaml('tmp.yaml')
    al1 = AList()
    al1.load_yaml('tmp.yaml')

    assert al0 == al1

