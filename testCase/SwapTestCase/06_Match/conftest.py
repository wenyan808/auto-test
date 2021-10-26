#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020/7/31
# @Author  : yuhuiqing



def pytest_generate_tests(metafunc: "Metafunc"):
    """ generate (multiple) parametrized calls to a test function."""
    if "params" in metafunc.fixturenames:
        metafunc.parametrize("params",
                             metafunc.module.params,
                             ids=metafunc.module.caseNames,
                             scope="function")