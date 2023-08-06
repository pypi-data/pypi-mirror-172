from pyConfObj import ConfObj, ConfObjList


class A(ConfObj):
    atr_int = None
    atr_str = None


dump_a = {
    "atr_int": 3,
    "atr_str": "Whatever"}
dump_a_err = {
    "atr_int": 3,
    "atr_str": "Whatever",
    "atr_unknown": None
}
json_a = """{
  "atr_int": 3,
  "atr_str": "Whatever"
}"""
yaml_a = b'atr_int: 3\natr_str: Whatever\n'


class B(ConfObj):
    atr_a = A()
    atr_int = None

    def check_pass(self) -> bool:
        if isinstance(self.atr_int, int):
            # arbitrary, just to have an easy way to make it fail
            if self.atr_int < 100:
                return True
        return False


class AList(ConfObj):
    alist = None

    def __init__(self):
        super().__init__()
        self.alist = ConfObjList(A)


class BList(ConfObj):
    blist = None
    atr_str = None

    def __init__(self):
        super().__init__()
        self.blist = ConfObjList(B)

    def check_pass(self) -> bool:
        if self.atr_str in (None, ""):
            return False
        return True


dump_blist = {'atr_str': 'y', 'blist': [{'atr_a': {'atr_int': None, 'atr_str': None}, 'atr_int': None},
                                        {'atr_a': {'atr_int': 3, 'atr_str': 'w'}, 'atr_int': 34}]}
