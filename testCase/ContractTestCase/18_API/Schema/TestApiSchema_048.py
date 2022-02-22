#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/11/22
# @Author  : Alex Li
"""

所属分组
    反向交割 API 测试
用例标题
    合约闪电平仓下单
前置条件

步骤/文本
    1.调用接口：api/v1/lightning_close_position
预期结果
    A)接口返回的json格式、字段名、字段值正确
优先级
    1
"""
import time
from pprint import pprint

import allure
import pytest
from common.util import get_contract_type
from common.ContractServiceAPI import t as contract_api
from schema import Or, Schema
from tool.atp import ATP


@allure.epic('反向交割')  # 这里填业务线
@allure.feature('API 测试')  # 这里填功能
@allure.story('合约闪电平仓下单')  # 这里填子功能，没有的话就把本行注释掉
@allure.tag('Script owner : Alex Li', 'Case owner : Alex Li')
@pytest.mark.stable
class TestApiSchema_048:

    @allure.step('前置条件')
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, symbol):
        print("前置条件 {}".format(symbol))
        ATP.make_market_depth(volume=2, depth_count=5)

    @allure.title('合约闪电平仓下单')
    @allure.step('测试执行')
    def test_execute(self, symbol, symbol_period):
        with allure.step('1、调用接口：api/v1/lightning_close_position'):
            pass
        with allure.step('2、接口返回的json格式、字段名、字段值正确'):
            # 构造持仓量
            price = ATP.get_current_price()
            contract_type = get_contract_type(symbol_period)
            sell_order = contract_api.contract_order(
                symbol=symbol, contract_type=contract_type, price=price, volume=1, direction="sell", offset="open")
            pprint(sell_order)
            buy_order = contract_api.contract_order(
                symbol=symbol, contract_type=contract_type, price=price, volume=1, direction="buy", offset="open")
            pprint(buy_order)
            time.sleep(2)
            res = contract_api.lightning_close_position(
                symbol=symbol, contract_type=contract_type, volume=1, direction="buy")
            print(res)

            schema = {
                "status": "ok",
                "data": {
                    "order_id": int,
                    "order_id_str": str
                },
                "ts": int
            }
            Schema(schema).validate(res)

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')
        print(ATP.cancel_all_types_order())
        print(ATP.close_all_position())


if __name__ == '__main__':
    pytest.main()
