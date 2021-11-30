#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/11/22
# @Author  : Alex Li
"""

所属分组
    反向交割 API 测试
用例标题
    获取用户的合约当前未成交委托
前置条件

步骤/文本
    1.调用接口：api/v1/contract_openorders
预期结果
    A)接口返回的json格式、字段名、字段值正确
优先级
    1
"""


import allure
import pytest
from common.ContractServiceAPI import common_user_contract_service_api as common_contract_api
from common.ContractServiceAPI import t as contract_api
from schema import Or, Schema
from tool.atp import ATP


@allure.epic('反向交割')  # 这里填业务线
@allure.feature('API 测试')  # 这里填功能
@allure.story('获取用户的合约当前未成交委托')  # 这里填子功能，没有的话就把本行注释掉
@allure.tag('Script owner : Alex Li', 'Case owner : Alex Li')
@pytest.mark.stable
class TestApiSchema_043:

    @allure.step('前置条件')
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, symbol):
        print("前置条件 {}".format(symbol))
        print(ATP.make_market_depth())
        print(ATP.cancel_all_order())
        # 切回持仓倍数
        res = contract_api.contract_switch_lever_rate(
            symbol="BTC", lever_rate=5)
        print(res)

    @allure.title('获取用户的合约当前未成交委托')
    @allure.step('测试执行')
    def test_execute(self, sub_uid):
        with allure.step('1、调用接口：api/v1/contract_openorders'):
            pass
        with allure.step('2、接口返回的json格式、字段名、字段值正确'):
            # 构造持仓量
            price = ATP.get_current_price()
            res_sell = contract_api.contract_order(
                symbol="BTC", contract_type="this_week", price=price+10, volume=1, direction="sell", offset="open")
            print(res_sell)
            res = contract_api.contract_openorders(symbol="BTC")
            print(res)
            if res["status"] != "error":
                schema = {
                    "status": "ok",
                    "data": {
                        "orders": [
                            {
                                "symbol": str,
                                "contract_code": str,
                                "contract_type": str,
                                "volume": int,
                                "price": Or(float, int),
                                "order_price_type": str,
                                "order_type": int,
                                "direction": str,
                                "offset": str,
                                "lever_rate": int,
                                "order_id": int,
                                "client_order_id": Or(float, int, None),
                                "created_at": int,
                                "trade_volume": Or(float, int),
                                "trade_turnover": Or(float, int),
                                "fee": Or(float, int),
                                "trade_avg_price": Or(float, int, None),
                                "margin_frozen": Or(float, int),
                                "profit": Or(float, int),
                                "status": Or(float, int),
                                "order_source": str,
                                "order_id_str": str,
                                "fee_asset": str,
                                "liquidation_type": Or(float, int, None),
                                "canceled_at": Or(float, int, None),
                                "is_tpsl": int,
                                "update_time": int,
                                "real_profit": Or(float, int)
                            }
                        ],
                        "total_page": int,
                        "current_page": int,
                        "total_size": int
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
