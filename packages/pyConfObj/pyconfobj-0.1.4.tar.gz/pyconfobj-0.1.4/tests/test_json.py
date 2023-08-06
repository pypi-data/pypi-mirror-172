from definitions import *


def test_confobj_json():
    a0 = A()
    a0.atr_int = 3
    a0.atr_str = "Whatever"
    b0 = B()
    b0.atr_a = a0
    b0.atr_int = 4
    b1 = B()
    b0.save_as_json('tmp.json')
    b1.load_json('tmp.json')
    assert b0 == b1


def test_confobjlist_json():
    al0 = AList()
    a0 = A()
    a0.atr_int = 3
    a0.atr_str = "Whatever"
    a1 = A()
    a1.atr_int = 55
    a1.atr_str = "Whenever"
    al0.alist.append(a0)
    al0.alist.append(a1)
    al0.save_as_json('tmp.json')
    al1 = AList()
    al1.load_json('tmp.json')

    assert al0 == al1

