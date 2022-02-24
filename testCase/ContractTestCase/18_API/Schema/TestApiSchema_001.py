#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/11/22
# @Author  : Alex Li
"""

所属分组
    反向交割 API 测试
用例标题
    获取合约信息
前置条件

步骤/文本
    1.调用接口：api/v1/contract_contract_info
预期结果
    A)接口返回的json格式、字段名、字段值正确
优先级
    1
"""
from pprint import pprint

import allure
from common.util import get_contract_type
import pytest
from schema import Schema, Or
from common.ContractServiceAPI import t as contract_api


@allure.epic('反向交割')  # 这里填业务线
@allure.feature('API 测试')  # 这里填功能
@allure.story('获取合约信息')  # 这里填子功能，没有的话就把本行注释掉
@allure.tag('Script owner : Alex Li', 'Case owner : Alex Li')
@pytest.mark.stable
class TestApiSchema_001:

    @allure.step('前置条件')
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, symbol):
        print("前置条件 {}".format(symbol))

    @allure.title('获取合约信息')
    @allure.step('测试执行')
    def test_execute(self, symbol, symbol_period):
        with allure.step('1、调用接口：api/v1/contract_contract_info'):
            pass
        with allure.step('2、接口返回的json格式、字段名、字段值正确'):
            contract_type = get_contract_type(symbol_period)
            res = contract_api.contract_contract_info(
                symbol=symbol, contract_type=contract_type)
            pprint(res)
            schema = {
                "status": "ok",
                "data": [
                    {
                        "symbol": symbol,
                        "contract_code": str,
                        "contract_type": contract_type,
                        "contract_size": Or(float, int),
                        "price_tick": Or(float, int),
                        "delivery_date": str,
                        "delivery_time": str,
                        "create_date": str,
                        "contract_status": int,
                        "settlement_time": str
                    }
                ],
                "ts": int
            }
            Schema(schema).validate(res)

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')


if __name__ == '__main__':
    pytest.main()
