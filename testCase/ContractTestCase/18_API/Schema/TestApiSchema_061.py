#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/11/22
# @Author  : Alex Li
"""

所属分组
    反向交割 API 测试
用例标题
    跟踪委托撤单
前置条件

步骤/文本
    1.调用接口：api/v1/contract_track_cancel
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
@allure.story('跟踪委托撤单')  # 这里填子功能，没有的话就把本行注释掉
@allure.tag('Script owner : Alex Li', 'Case owner : Alex Li')
@pytest.mark.stable
class TestApiSchema_061:

    @allure.step('前置条件')
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, symbol):
        print("前置条件 {}".format(symbol))
        print(ATP.make_market_depth())

    @allure.title('跟踪委托撤单')
    @allure.step('测试执行')
    def test_execute(self, sub_uid):
        with allure.step('1、调用接口：api/v1/contract_track_cancel'):
            pass
        with allure.step('2、接口返回的json格式、字段名、字段值正确'):
            # 构造持仓量
            price = ATP.get_current_price()
            common_contract_api.contract_order(
                symbol="BTC", contract_type="this_week", price=price, volume=5, direction="buy", offset="open")
            contract_api.contract_trigger_order(
                symbol="BTC", contract_type="this_week", trigger_type="ge", trigger_price=price, order_price=price+1, volume=1, direction="buy", offset="open", lever_rate=5)
            res_sell = contract_api.contract_track_order(
                symbol="BTC", contract_type="this_week", direction="sell", offset="open", lever_rate=5, volume=1, active_price=price+1, callback_rate=0.01, order_price_type="optimal_5")
            print(res_sell)

            res = contract_api.contract_track_cancel(
                symbol="BTC", order_id=res_sell["data"]["order_id"])
            assert res['status'] == 'ok'
            assert common.util.compare_dictkey(
                ["errors", "successes"], res["data"])

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')
        print(ATP.clean_market())
        print(ATP.cancel_all_order())


if __name__ == '__main__':
    pytest.main()
