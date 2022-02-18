#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/11/22
# @Author  : Alex Li
"""

所属分组
    反向交割 API 测试
用例标题
    合约批量下单
前置条件

步骤/文本
    1.调用接口：api/v1/contract_batchorder
预期结果
    A)接口返回的json格式、字段名、字段值正确
优先级
    1
"""
from pprint import pprint

import allure
import pytest
from schema import Schema

from common.ContractServiceAPI import t as contract_api
from tool.atp import ATP


@allure.epic('反向交割')  # 这里填业务线
@allure.feature('API 测试')  # 这里填功能
@allure.story('合约批量下单')  # 这里填子功能，没有的话就把本行注释掉
@allure.tag('Script owner : Alex Li', 'Case owner : Alex Li')
@pytest.mark.stable
class TestApiSchema_037:

    @allure.step('前置条件')
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, symbol):
        print("前置条件 {}".format(symbol))

    @allure.title('合约批量下单')
    @allure.step('测试执行')
    def test_execute(self, symbol):
        with allure.step('1、调用接口：api/v1/contract_batchorder'):
            pass
        with allure.step('2、接口返回的json格式、字段名、字段值正确'):
            # 构造持仓量
            price = ATP.get_current_price()
            res = contract_api.contract_batchorder(
                {"orders_data": [{"symbol": symbol, "contract_type": "this_week", "volume": 1,
                                  "price": price, "direction": "buy", "offset": "open",
                                  "leverRate": 5, "orderPriceType": "limit"},
                                 {"symbol": 'symbol', "contract_type": "this_week", "volume": 1,
                                  "price": price, "direction": "buy", "offset": "open",
                                  "leverRate": 5, "orderPriceType": "limit"}
                                 ]})
            pprint(res)

            schema = {"data": {"errors": [{"index": int,
                                           "err_code": int,
                                           "err_msg": str}],
                               "success": [{"order_id": int,
                                            "index": int,
                                            "order_id_str": str}]
                               },
                      "status": "ok",
                      "ts": int}
            Schema(schema).validate(res)

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')
        print(ATP.cancel_all_order())


if __name__ == '__main__':
    pytest.main()
