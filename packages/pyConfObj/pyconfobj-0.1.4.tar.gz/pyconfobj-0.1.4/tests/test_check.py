from definitions import *


def test_conf_custom_check():
    a0 = A()
    b0 = B()
    b0.atr_a = a0
    assert not b0.check()
    b0.atr_int = 75
    assert b0.check()
    b0.atr_int = 110
    assert not b0.check()


def test_confobjlist_check():
    b0 = B()
    b1 = B()
    bl = BList()
    bl.blist.append(b0)
    bl.blist.append(b1)
    # Missing valid values for B instances and BList.str_str is None
    assert not bl.check()
    b0.atr_int = 75
    b1.atr_int = 99
    assert not bl.check()
    bl.atr_str = ""
    assert not bl.check()
    bl.atr_str = "w"
    assert bl.check()
    b0.atr_int = 110
    assert not bl.check()