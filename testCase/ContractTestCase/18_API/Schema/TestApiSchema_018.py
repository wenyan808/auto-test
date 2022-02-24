#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/11/22
# @Author  : Alex Li
"""

所属分组
    反向交割 API 测试
用例标题
    获取用户的合约持仓信息
前置条件

步骤/文本
    1.调用接口：api/v1/contract_position_info
预期结果
    A)接口返回的json格式、字段名、字段值正确
优先级
    1
"""
import time
from pprint import pprint

import allure
from common.util import get_contract_type
import pytest
from common.ContractServiceAPI import common_user_contract_service_api as common_contract_api
from common.ContractServiceAPI import t as contract_api
from schema import Or, Schema
from tool.atp import ATP


@allure.epic('反向交割')  # 这里填业务线
@allure.feature('API 测试')  # 这里填功能
@allure.story('获取用户的合约账户信息')  # 这里填子功能，没有的话就把本行注释掉
@allure.tag('Script owner : Alex Li', 'Case owner : Alex Li')
@pytest.mark.stable
class TestApiSchema_018:

    @allure.step('前置条件')
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, symbol):
        print("前置条件 {}".format(symbol))

    @allure.title('获取用户的合约账户信息')
    @allure.step('测试执行')
    def test_execute(self, symbol, symbol_period):
        with allure.step('1、调用接口：api/v1/contract_position_info'):
            pass
        with allure.step('2、接口返回的json格式、字段名、字段值正确'):
            # 构造持仓量
            contract_type = get_contract_type(symbol_period)
            price = ATP.get_current_price()
            contract_api.contract_order(
                symbol=symbol, contract_type=contract_type, price=price, volume=1, direction="buy", offset="open")
            contract_api.contract_order(
                symbol=symbol, contract_type=contract_type, price=price, volume=1, direction="sell", offset="open")
            time.sleep(1)
            res = contract_api.contract_position_info(
                symbol=symbol)
            pprint(res)
            if res["status"] != 'error':
                schema = {
                    "status": "ok",
                    "data": [
                        {
                            "symbol": symbol,
                            "contract_code": str,
                            "contract_type": str,
                            "volume": Or(float, int),
                            "available": Or(float, int),
                            "frozen": Or(float, int),
                            "cost_open": Or(float, int),
                            "cost_hold": Or(float, int),
                            "profit_unreal": Or(float, int),
                            "profit_rate": Or(float, int),
                            "lever_rate": Or(float, int),
                            "position_margin": Or(float, int),
                            "direction": str,
                            "profit": Or(float, int),
                            "last_price": Or(float, int),
                        }
                    ],
                    "ts": int
                }
                Schema(schema).validate(res)

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')
        print(ATP.cancel_all_order())
        print(ATP.close_all_position())


if __name__ == '__main__':
    pytest.main()
