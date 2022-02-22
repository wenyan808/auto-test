#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/11/22
# @Author  : Alex Li
"""

所属分组
    反向交割 API 测试
用例标题
    对仓位设置止盈止损订单
前置条件

步骤/文本
    1.调用接口：api/v1/contract_tpsl_order
预期结果
    A)接口返回的json格式、字段名、字段值正确
优先级
    1
"""
import time
from pprint import pprint

import allure
import pytest
from schema import Schema

from common.ContractServiceAPI import t as contract_api
from common.util import get_contract_type
from tool.atp import ATP


@allure.epic('反向交割')  # 这里填业务线
@allure.feature('API 测试')  # 这里填功能
@allure.story('对仓位设置止盈止损订单')  # 这里填子功能，没有的话就把本行注释掉
@allure.tag('Script owner : Alex Li', 'Case owner : Alex Li')
@pytest.mark.stable
class TestApiSchema_054:

    @allure.step('前置条件')
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, symbol):
        print("前置条件 {}".format(symbol))

    @allure.title('对仓位设置止盈止损订单')
    @allure.step('测试执行')
    def test_execute(self, symbol, symbol_period):
        with allure.step('1、调用接口：api/v1/contract_tpsl_order'):
            pass
        with allure.step('2、接口返回的json格式、字段名、字段值正确'):
            # 构造持仓量
            contract_type = get_contract_type(symbol_period)
            lastprice = ATP.get_current_price()
            tp_price = ATP.get_adjust_price(rate=1.05)
            sl_price = ATP.get_adjust_price(rate=0.95)

            buy_order = contract_api.contract_order(
                symbol=symbol, contract_type=contract_type, price=lastprice, volume=1, direction="buy", offset="open")
            pprint(buy_order)
            sell_order = contract_api.contract_order(
                symbol=symbol, contract_type=contract_type, price=lastprice, volume=1, direction="sell", offset="open")
            pprint(sell_order)
            time.sleep(2)

            res = contract_api.contract_tpsl_order(symbol=symbol,
                                                   contract_type=contract_type,
                                                   direction="sell",
                                                   volume=1,
                                                   tp_trigger_price=tp_price,
                                                   tp_order_price=tp_price,
                                                   tp_order_price_type="limit",
                                                   sl_trigger_price=sl_price,
                                                   sl_order_price=sl_price,
                                                   sl_order_price_type="limit")
            time.sleep(1)
            pprint(res)

            schema = {"data": {"tp_order": {"order_id": int,
                                            "order_id_str": str},
                               "sl_order": {"order_id": int,
                                            "order_id_str": str}
                               },
                      "status": "ok",
                      "ts": int}
            Schema(schema).validate(res)

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')
        print(ATP.cancel_all_tpsl_order())
        print(ATP.cancel_all_order())
        print(ATP.close_all_position())


if __name__ == '__main__':
    pytest.main()
