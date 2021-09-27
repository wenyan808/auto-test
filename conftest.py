#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020/8/19
# @Author  : zhangranghan
import os
import pathlib
import time

import allure
import pytest
import yaml
from _pytest.nose import teardown_nose

from config import conf
from tool.DingDingMsg import DingDingMsg
from tool.atp import ATP

"""
conftest.py文件名字是固定的，不可以做任何修改
不需要import导入conftest.py，pytest用例会自动识别该文件，若conftest.py文件放在根目录下，那么conftest.py作用于整个目录，全局调用
在不同的测试子目录也可以放conftest.py，其作用范围只在该层级以及以下目录生效
所有目录内的测试文件运行前都会先执行该目录下所包含的conftest.py文件
conftest.py文件不能被其他文件导入

"""


def pytest_collection_modifyitems(items):
    """
    测试用例收集完成时，将收集到的item的name和nodeid的中文显示在控制台上
    :return:
    """
    for item in items:
        item.name = item.name.encode("utf-8").decode("unicode_escape")
        item._nodeid = item.nodeid.encode("utf-8").decode("unicode_escape")


def pytest_sessionfinish():
    """
    读取application.yml文件中的配置信息
    将信息写到environment.properties中用于在allure报告中展
    :return:
    """
    path = pathlib.Path(__file__).parent / 'report/allure'
    if not path.exists():
        path.mkdir()
    with open(path / 'environment.properties', 'w') as f:
        f.write(
            "ENV={}\nSYSTEM_TYPE={}\nURL={}\nACCESS_KEY={}\nSECRET_KEY={}".format(conf.ENV, conf.SYSTEM_TYPE, conf.URL,
                                                                                  conf.ACCESS_KEY, conf.SECRET_KEY))


"""
1.把测试的结果.改成√，F改成x
2.命令行加个--change参数开关，默认不开启，当加上参数`--change on·的时候才生效
"""


def pytest_addoption(parser):
    parser.addoption(
        "--change",
        action="store",
        default="off",
        help="'Default 'off' for change, option: on or off"
    )


def pytest_report_teststatus(report, config):
    '''turn . into √，turn F into x, turn E into 0'''
    if config.getoption("--change") == "on":
        if report.when == 'call' and report.failed:
            return (report.outcome, 'x', 'failed')
        if report.when == 'call' and report.passed:
            return (report.outcome, '√', 'passed')


def pytest_generate_tests(metafunc: "Metafunc"):
    """ generate (multiple) parametrized calls to a test function."""
    if "api_test_data" in metafunc.fixturenames:
        test_case_name = metafunc.definition.name
        api_test_data_list = ATP.get_api_test_data(test_case_name)
        metafunc.parametrize("api_test_data", api_test_data_list,
                             scope="function")


@pytest.mark.hookwrapper
def pytest_runtest_setup(item):
    outcome = yield
    if outcome.excinfo:
        item.session._setupstate.addfinalizer((lambda: teardown_nose(item)), item)


@pytest.mark.hookwrapper
def pytest_runtest_makereport(item):
    outcome = yield
    report = outcome.get_result()
    if report.when == 'call':
        api_test_data = item.funcargs.get("api_test_data", {})
        if api_test_data:
            title = api_test_data.get("title", "")
            if title:
                allure.dynamic.title(title)
