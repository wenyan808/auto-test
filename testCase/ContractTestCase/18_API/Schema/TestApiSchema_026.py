#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/11/22
# @Author  : Alex Li
"""

所属分组
    反向交割 API 测试
用例标题
    查询用户结算记录
前置条件

步骤/文本
    1.调用接口：api/v1/contract_user_settlement_records
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
@allure.story('查询用户结算记录')  # 这里填子功能，没有的话就把本行注释掉
@allure.tag('Script owner : Alex Li', 'Case owner : Alex Li')
@pytest.mark.stable
class TestApiSchema_026:

    @allure.step('前置条件')
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, symbol):
        print("前置条件 {}".format(symbol))

    @allure.title('组合查询用户财务记录')
    @allure.step('测试执行')
    def test_execute(self, symbol):
        with allure.step('1、调用接口：api/v1/contract_user_settlement_records'):
            pass
        with allure.step('2、接口返回的json格式、字段名、字段值正确'):
            # 构造持仓量

            res = contract_api.contract_user_settlement_records(symbol=symbol)
            pprint(res)

            schema = {"data": {"total_page": int,
                               "current_page": int,
                               "total_size": int,
                               "settlement_records": [{"symbol": str,
                                                       "margin_balance_init": Or(float, int, None),
                                                       "margin_balance": Or(float, int, None),
                                                       "settlement_profit_real": Or(float, int, None),
                                                       "settlement_time": int,
                                                       "clawback": Or(float, int, None),
                                                       "delivery_fee": Or(float, int, None),
                                                       "offset_profitloss": Or(float, int, None),
                                                       "fee": Or(float, int, None),
                                                       "fee_asset": str,
                                                       "positions": [{"symbol": str,
                                                                      "contract_code": str,
                                                                      "direction": str,
                                                                      "volume": Or(float, int, None),
                                                                      "cost_open": Or(float, int, None),
                                                                      "cost_hold_pre": Or(float, int, None),
                                                                      "cost_hold": Or(float, int, None),
                                                                      "settlement_profit_unreal": Or(float, int, None),
                                                                      "settlement_price": Or(float, int, None),
                                                                      "settlement_type": str}]
                                                       }]
                               },
                      "status": "ok",
                      "ts": int}
            Schema(schema).validate(res)

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')


if __name__ == '__main__':
    pytest.main()
