#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Otger Ballester'
__copyright__ = 'Copyright 2022'
__date__ = '18/10/22'
__credits__ = ['Otger Ballester', ]
__license__ = 'MIT License'
__version__ = '0.1.5'
__maintainer__ = 'Otger Ballester'
__email__ = 'otger@ifae.es'

import inspect
import json
import yaml
from collections import UserList


class ConfObj:
    def __init__(self):
        self._loaded = {}

    def load_dump(self, dump):
        if not isinstance(dump, dict):
            raise Exception('Configuration must be a dictionary')

        for k in dump.keys():
            try:
                a = getattr(self, k)
                if not inspect.ismethod(a):
                    if isinstance(a, (ConfObj, ConfObjList)):
                        a.load_dump(dump[k])
                    else:
                        setattr(self, k, dump[k])
            except AttributeError:
                pass

    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False
        for mem in inspect.getmembers(self):
            if not mem[0].startswith('_') and not inspect.ismethod(mem[1]):
                if getattr(self, mem[0]) != getattr(other, mem[0]):
                    return False
        return True

    def dump(self):
        t = {}
        for mem in inspect.getmembers(self):
            if not mem[0].startswith('_') and not inspect.ismethod(mem[1]):
                if isinstance(mem[1], (ConfObj, ConfObjList)):
                    t[mem[0]] = mem[1].dump()
                else:
                    t[mem[0]] = mem[1]
        return t

    def as_json(self):
        return json.dumps(self.dump(), indent=2)

    def as_yaml(self):
        return yaml.dump(self.dump(), indent=2, encoding="utf-8")

    def load_json(self, json_path):
        with open(json_path, 'r') as json_file:
            self._loaded = json.load(json_file)
            self.load_dump(self._loaded)

    def save_as_json(self, json_path):
        with open(json_path, 'w') as json_file:
            json.dump(self.dump(), json_file, indent=2)

    def load_yaml(self, yaml_path):
        with open(yaml_path, 'r') as yaml_fp:
            self._loaded = yaml.safe_load(yaml_fp)
            self.load_dump(self._loaded)

    def save_as_yaml(self, yaml_path):
        with open(yaml_path, 'w') as yaml_fp:
            yaml.dump(self.dump(), yaml_fp, indent=2, encoding="utf-8")

    def check_pass(self) -> bool:
        """
        To be overwritten when a child class wants to implement a valid configuration check
        """
        return True

    def check(self) -> bool:
        """
        Return if all checks have passed
        For it to work, any 
        """
        if not self.check_pass() is True:
            return False
        # Check for any confObj instances if check has not already failed
        for mem in inspect.getmembers(self):
            if not mem[0].startswith('_') and not inspect.ismethod(mem[1]):
                if isinstance(mem[1], (ConfObj, ConfObjList)):
                    if not mem[1].check() is True:
                        return False
        return True


class ConfObjList(UserList, ConfObj):

    def __init__(self, conf_type):
        super().__init__()
        if not issubclass(conf_type, ConfObj):
            raise Exception("The type of elements to store on the ConfObjList must inherit from ConfObj")
        self._confType = conf_type

    def append(self, element):
        if not isinstance(element, self._confType):
            raise Exception(f"Lists items must be of type {self._confType}")
        super().append(element)

    def __setitem__(self, i, item):
        if not isinstance(item, self._confType):
            raise Exception(f"Lists items must be of type {self._confType}")
        super().__setitem__(i, item)

    def check(self):
        for el in self.data:
            if el.check() is not True:
                return False
        return True

    def dump(self):
        tmp = []
        for el in self.data:
            tmp.append(el.dump())
        return tmp

    def load_dump(self, dump):
        # dump must be a list of dicts
        if not isinstance(dump, list):
            raise Exception('Configuration must be a list for ConfObjList')

        for el in dump:
            tmp = self._confType()
            tmp.load_dump(el)
            self.data.append(tmp)

    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False
        if self._confType != other._confType:
            return False
        if len(self.data) != len(other.data):
            return False
        for i, el in enumerate(self.data):
            if el not in other.data:
                return False
        return True
