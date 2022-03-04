#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/11/22
# @Author  : Alex Li
"""

所属分组
    反向交割 API 测试
用例标题
    获取用户的合约订单信息
前置条件

步骤/文本
    1.调用接口：api/v1/contract_order_info
预期结果
    A)接口返回的json格式、字段名、字段值正确
优先级
    1
"""

import allure
import pytest
from schema import Or, Schema
from common.util import get_contract_type
from common.ContractServiceAPI import t as contract_api
from tool.atp import ATP


@allure.epic('反向交割')  # 这里填业务线
@allure.feature('API 测试')  # 这里填功能
@allure.story('获取用户的合约订单信息')  # 这里填子功能，没有的话就把本行注释掉
@allure.tag('Script owner : Alex Li', 'Case owner : Alex Li')
@pytest.mark.stable
class TestApiSchema_041:

    @allure.step('前置条件')
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, symbol):
        print("前置条件 {}".format(symbol))
        # 切回持仓倍数

    @allure.title('获取用户的合约订单信息')
    @allure.step('测试执行')
    def test_execute(self, symbol, symbol_period):
        with allure.step('1、调用接口：api/v1/contract_order_info'):
            pass
        with allure.step('2、接口返回的json格式、字段名、字段值正确'):
            # 构造持仓量
            contract_type = get_contract_type(symbol_period)
            price = ATP.get_current_price()
            contract_api.contract_order(
                symbol=symbol, contract_type=contract_type, price=price, volume=1, direction="buy", offset="open")
            res_temp = contract_api.contract_order(
                symbol=symbol, contract_type=contract_type, price=price, volume=1, direction="sell", offset="open")
            order_id = res_temp["data"]["order_id"]
            res = contract_api.contract_order_info(symbol=symbol, order_id=order_id)
            print(res)
            schema = {
                "status": "ok",
                "data": [
                    {
                        "symbol": str,
                        "contract_code": str,
                        "contract_type": str,
                        "volume": Or(float, int),
                        "price": Or(float, int),
                        "order_price_type": str,
                        "order_type": int,
                        "direction": str,
                        "offset": str,
                        "lever_rate": Or(float, int),
                        "order_id": int,
                        "client_order_id": Or(float, int, None),
                        "created_at": int,
                        "trade_volume": Or(float, int),
                        "trade_turnover": Or(float, int),
                        "fee": Or(float, int),
                        "trade_avg_price": Or(float, int, None),
                        "margin_frozen": Or(float, int),
                        "profit": Or(float, int),
                        "status": int,
                        "order_source": str,
                        "order_id_str": str,
                        "real_profit": int,
                        "fee_asset": str,
                        "liquidation_type": str,
                        "canceled_at": int,
                        "is_tpsl": int}
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
