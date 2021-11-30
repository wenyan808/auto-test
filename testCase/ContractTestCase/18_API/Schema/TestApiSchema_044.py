#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/11/22
# @Author  : Alex Li
"""

所属分组
    反向交割 API 测试
用例标题
    获取用户的合约历史委托
前置条件

步骤/文本
    1.调用接口：api/v1/contract_hisorders
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
from tool.atp import ATP


@allure.epic('反向交割')  # 这里填业务线
@allure.feature('API 测试')  # 这里填功能
@allure.story('获取用户的合约历史委托')  # 这里填子功能，没有的话就把本行注释掉
@allure.tag('Script owner : Alex Li', 'Case owner : Alex Li')
@pytest.mark.stable
class TestApiSchema_044:

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

    @allure.title('获取用户的合约历史委托')
    @allure.step('测试执行')
    def test_execute(self, sub_uid):
        with allure.step('1、调用接口：api/v1/contract_hisorders'):
            pass
        with allure.step('2、接口返回的json格式、字段名、字段值正确'):
            # 构造持仓量
            price = ATP.get_current_price()
            common_contract_api.contract_order(
                symbol="BTC", contract_type="this_week", price=price, volume=1, direction="buy", offset="open")
            res_sell = contract_api.contract_order(
                symbol="BTC", contract_type="this_week", price=price+100, volume=3, direction="sell", offset="open")
            print(res_sell)
            res = contract_api.contract_hisorders(
                symbol="BTC", trade_type=0, type=1, status=0, create_date=30)
            print(res)
            assert res['status'] == 'ok'
            assert common.util.compare_dictkey(
                ["order_id", "contract_code", "symbol", "lever_rate", "direction", "offset", "volume", "price", "create_date", "update_time",
                 "order_source", "order_price_type", "order_type", "margin_frozen", "profit", "contract_type", "trade_volume", "trade_turnover",
                 "fee", "trade_avg_price", "status", "order_id_str", "fee_asset", "liquidation_type", "is_tpsl", "real_profit"], res["data"]["orders"][0])

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')
        print(ATP.clean_market())
        print(ATP.cancel_all_order())


if __name__ == '__main__':
    pytest.main()
