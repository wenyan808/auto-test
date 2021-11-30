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


import allure
import common.util
import pytest
from common.ContractServiceAPI import common_user_contract_service_api as common_contract_api
from common.ContractServiceAPI import t as contract_api
from schema import Or, Schema
from tool.atp import ATP


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
        print(ATP.make_market_depth())

    @allure.title('组合查询用户财务记录')
    @allure.step('测试执行')
    def test_execute(self, sub_uid):
        with allure.step('1、调用接口：api/v1/contract_user_settlement_records'):
            pass
        with allure.step('2、接口返回的json格式、字段名、字段值正确'):
            # 构造持仓量
            price = ATP.get_current_price(contract_code="BTC")
            common_contract_api.contract_order(
                symbol="BTC", contract_type="this_week", price=price, volume=1, direction="buy", offset="open")
            contract_api.contract_order(
                symbol="BTC", contract_type="this_week", price=price, volume=1, direction="sell", offset="open")
            res = contract_api.contract_user_settlement_records(
                symbol="BTC")
            print(res)
            if res["status"] != "error":
                schema = {
                    "status": "ok",
                    "data": {
                        "total_page": int,
                        "current_page": int,
                        "total_size": int,
                        "settlement_records": [
                            {
                                "symbol": str,
                                "margin_balance_init": Or(float, int, None),
                                "margin_balance": Or(float, int, None),
                                "settlement_profit_real": Or(float, int, None),
                                "settlement_time": int,
                                "clawback": Or(float, int, None),
                                "delivery_fee": Or(float, int, None),
                                "offset_profitloss": Or(float, int, None),
                                "fee": Or(float, int, None),
                                "fee_asset": str,
                                "positions": [
                                    {
                                        "symbol": str,
                                        "contract_code": str,
                                        "direction": str,
                                        "volume": Or(float, int, None),
                                        "cost_open": Or(float, int, None),
                                        "cost_hold_pre": Or(float, int, None),
                                        "cost_hold": Or(float, int, None),
                                        "settlement_profit_unreal": Or(float, int, None),
                                        "settlement_price": Or(float, int, None),
                                        "settlement_type": str
                                    }
                                ]
                            }
                        ]
                    },
                    "ts": int
                }
                Schema(schema).validate(res)

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')
        print(ATP.clean_market())
        print(ATP.cancel_all_order())


if __name__ == '__main__':
    pytest.main()
