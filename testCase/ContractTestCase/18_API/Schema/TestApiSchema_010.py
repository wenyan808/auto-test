#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/11/22
# @Author  : Alex Li
"""

所属分组
    反向交割 API 测试
用例标题
    获取平台阶梯保证金
前置条件

步骤/文本
    1.调用接口：api/v1/contract_ladder_margin
预期结果
    A)接口返回的json格式、字段名、字段值正确
优先级
    1
"""
from pprint import pprint

import allure
import pytest
from schema import Or, Schema

from common.ContractServiceAPI import t as contract_api


@allure.epic('反向交割')  # 这里填业务线
@allure.feature('API 测试')  # 这里填功能
@allure.story('获取平台阶梯保证金')  # 这里填子功能，没有的话就把本行注释掉
@allure.tag('Script owner : Alex Li', 'Case owner : Alex Li')
@pytest.mark.stable
class TestApiSchema_010:

    @allure.step('前置条件')
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, symbol):
        print("前置条件 {}".format(symbol))

    @allure.title('获取平台阶梯保证金')
    @allure.step('测试执行')
    def test_execute(self, symbol):
        with allure.step('1、调用接口：api/v1/contract_ladder_margin'):
            pass
        with allure.step('2、接口返回的json格式、字段名、字段值正确'):
            # 构造持仓量
            res = contract_api.contract_ladder_margin(symbol=symbol)
            pprint(res)

            schema = {"data": [{"symbol": symbol,
                                "list": [{"lever_rate": int,
                                          "ladders": [{"min_margin_balance": Or(float, int, None),
                                                       "max_margin_balance": Or(float, int, None),
                                                       "min_margin_available": Or(float, int, None),
                                                       "max_margin_available": Or(float, int, None)}]
                                          }]
                                }],
                      "status": "ok",
                      "ts": int}

            Schema(schema).validate(res)

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')


if __name__ == '__main__':
    pytest.main()
