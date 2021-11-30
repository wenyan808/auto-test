#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/11/22
# @Author  : Alex Li
"""

所属分组
    反向交割 API 测试
用例标题
    获取用户的合约订单明细信息
前置条件

步骤/文本
    1.调用接口：api/v1/contract_order_detail
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
@allure.story('获取用户的合约订单明细信息')  # 这里填子功能，没有的话就把本行注释掉
@allure.tag('Script owner : Alex Li', 'Case owner : Alex Li')
@pytest.mark.stable
class TestApiSchema_042:

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

    @allure.title('获取用户的合约订单明细信息')
    @allure.step('测试执行')
    def test_execute(self, sub_uid):
        with allure.step('1、调用接口：api/v1/contract_order_detail'):
            pass
        with allure.step('2、接口返回的json格式、字段名、字段值正确'):
            # 构造持仓量
            price = ATP.get_current_price()
            common_contract_api.contract_order(
                symbol="BTC", contract_type="this_week", price=price, volume=1, direction="buy", offset="open")
            res_sell = contract_api.contract_order(
                symbol="BTC", contract_type="this_week", price=price, volume=1, direction="sell", offset="open")
            res = contract_api.contract_order_detail(
                symbol="BTC", order_id=res_sell["data"]["order_id"])
            print(res)
            if res["status"] != "error":
                schema = {
                    "status": "ok",
                    "data": {
                        "symbol": str,
                        "contract_code": str,
                        "contract_type": str,
                        "instrument_price":  Or(float, int),
                        "final_interest":  Or(float, int),
                        "adjust_value":  Or(float, int),
                        "lever_rate":  Or(float, int),
                        "direction": str,
                        "offset": str,
                        "volume":  Or(float, int),
                        "price":  Or(float, int),
                        "created_at": int,
                        "canceled_at": int,
                        "order_source": str,
                        "order_price_type": str,
                        "margin_frozen": int,
                        "profit": int,
                        "trades": [
                            {
                                "trade_id": int,
                                "trade_price":  Or(float, int),
                                "trade_volume":  Or(float, int),
                                "trade_turnover":  Or(float, int),
                                "trade_fee":  Or(float, int),
                                "created_at": int,
                                "role": str,
                                "real_profit": int,
                                "profit": int,
                                "id": str
                            }
                        ],
                        "total_page": int,
                        "current_page": int,
                        "total_size": int,
                        "liquidation_type": str,
                        "fee_asset": str,
                        "order_id": int,
                        "order_id_str": str,
                        "client_order_id":  Or(float, int, None),
                        "order_type": str,
                        "status": int,
                        "trade_avg_price":  Or(float, int),
                        "trade_turnover":  Or(float, int),
                        "trade_volume":  Or(float, int),
                        "is_tpsl": int,
                        "real_profit": Or(float, int),
                        "fee": float
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
