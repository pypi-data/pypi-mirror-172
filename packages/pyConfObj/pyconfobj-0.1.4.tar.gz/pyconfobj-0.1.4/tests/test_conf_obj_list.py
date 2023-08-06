import pytest
from definitions import *


def test_load_dump_exc():
    b0 = BList()
    with pytest.raises(Exception) as e_info:
        b0.load_dump('perico')
    with pytest.raises(Exception) as e_info:
        b0.blist.load_dump({'perico': "los palotes"})


def test_blist_type_exc():
    with pytest.raises(Exception) as e_info:
        ConfObjList(int)


def test_append_exc():
    bl0 = BList()
    a0 = A()
    a0.atr_int = 4
    a0.atr_str = "Whenever"
    with pytest.raises(Exception) as e_info:
        bl0.blist.append(a0)


def test_set_item_exc():
    bl0 = BList()
    a0 = A()
    a0.atr_int = 4
    a0.atr_str = "Whenever"
    bl0.blist.append(B())
    with pytest.raises(Exception) as e_info:
        bl0.blist[0] = a0


def test_eq_diff_class():
    bl0 = BList()
    al0 = AList()
    assert bl0.blist != al0.alist


def test_eq_miss_item():
    bl0 = BList()
    b0 = B()
    bl0.atr_str = "str"
    b0.atr_a = A()
    b0.atr_a.atr_int = 4
    b0.atr_a.atr_str = "w"
    b0.atr_int = 3
    bl0.blist.append(b0)
    bl1 = BList()
    bl1.atr_str = "str"
    assert bl0 != bl1
    b1 = B()
    b1.atr_a = A()
    b1.atr_a.atr_int = 3
    b1.atr_a.atr_str = "w"
    b1.atr_int = 3
    bl1.blist.append(b1)
    assert bl0 != bl1
    b1.atr_a.atr_int = 4
    assert bl0 == bl1
    bl1.atr_str = "string"
    assert bl0 != bl1


def test_eq_diff_class_type():
    bl0 = BList()
    assert bl0.blist != 3


def test_set_item():
    bl0 = BList()
    bl0.blist.append(B())
    bl0.blist[0] = B()


def test_dump_load_dump_list():
    bl = BList()
    a0 = A()
    b0 = B()
    b1 = B()
    b1.atr_int = 34
    b1.atr_a = a0
    b1.atr_a.atr_int = 3
    b1.atr_a.atr_str = "w"
    bl.atr_str = "y"
    bl.blist.append(b0)
    bl.blist.append(b1)
    dump = bl.dump()
    blbis = BList()
    blbis.load_dump(dump)
    assert bl == blbis
