import pytest
from definitions import *


def test_load_dump_exc():
    a0 = A()
    with pytest.raises(Exception) as e_info:
        a0.load_dump('perico')
    # exception is silenced when extra fields are defined on the dump
    a0.load_dump(dump_a_err)


def test_load_dump():
    a0 = A()
    a0.load_dump(dump_a)

    a1 = A()
    a1.atr_int = 3
    a1.atr_str = "Whatever"
    assert a0 == a1


def test_asjson():
    a0 = A()
    a0.load_dump(dump_a)
    assert json_a == a0.as_json()


def test_asyaml():
    a0 = A()
    a0.load_dump(dump_a)
    assert yaml_a == a0.as_yaml()