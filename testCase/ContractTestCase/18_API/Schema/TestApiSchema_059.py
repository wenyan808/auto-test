#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/11/22
# @Author  : Alex Li
"""

所属分组
    反向交割 API 测试
用例标题
    查询开仓单关联的止盈止损订单详情
前置条件

步骤/文本
    1.调用接口：api/v1/contract_relation_tpsl_order
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
@allure.story('查询开仓单关联的止盈止损订单详情')  # 这里填子功能，没有的话就把本行注释掉
@allure.tag('Script owner : Alex Li', 'Case owner : Alex Li')
@pytest.mark.stable
class TestApiSchema_059:

    @allure.step('前置条件')
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, symbol):
        print("前置条件 {}".format(symbol))
        print(ATP.make_market_depth())

    @allure.title('查询开仓单关联的止盈止损订单详情')
    @allure.step('测试执行')
    def test_execute(self, sub_uid):
        with allure.step('1、调用接口：api/v1/contract_relation_tpsl_order'):
            pass
        with allure.step('2、接口返回的json格式、字段名、字段值正确'):
            # 构造持仓量
            price = ATP.get_current_price()
            common_contract_api.contract_order(
                symbol="BTC", contract_type="this_week", price=price, volume=5, direction="sell", offset="open")
            res_buy = contract_api.contract_trigger_order(
                symbol="BTC", contract_type="this_week", trigger_type="ge", trigger_price=price, order_price=price+1, volume=1, direction="buy", offset="open", lever_rate=5)
            print(res_buy)
            res = contract_api.contract_relation_tpsl_order(
                symbol="BTC", order_id=res_buy["data"]["order_id"])
            print(res)
            if res["status"] != "error":
                schema = {
                    "status": "ok",
                    "data": {
                        "symbol": str,
                        "contract_code": str,
                        "contract_type": str,
                        "volume": Or(float, int),
                        "price": int,
                        "order_price_type": str,
                        "direction": str,
                        "offset": str,
                        "lever_rate": Or(float, int),
                        "order_id": int,
                        "order_id_str": str,
                        "client_order_id": Or(float, int, None),
                        "created_at": int,
                        "trade_volume": Or(float, int),
                        "trade_turnover": Or(float, int),
                        "fee": Or(float, int),
                        "trade_avg_price": Or(float, int, None),
                        "margin_frozen": Or(float, int, None),
                        "profit": Or(float, int, None),
                        "status": int,
                        "order_type": int,
                        "order_source": str,
                        "fee_asset": str,
                        "canceled_at": int,
                        "tpsl_order_info": [
                            {
                                "volume": Or(float, int),
                                "direction": str,
                                "tpsl_order_type": str,
                                "order_id": int,
                                "order_id_str": str,
                                "trigger_type": str,
                                "trigger_price": int,
                                "order_price": Or(float, int),
                                "created_at": int,
                                "order_price_type": str,
                                "relation_tpsl_order_id": str,
                                "status": int,
                                "canceled_at": int,
                                "fail_code": Or(float, int, None),
                                "fail_reason": Or(float, int, None),
                                "triggered_price": Or(float, int, None),
                                "relation_order_id": str
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
