#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/11/22
# @Author  : Alex Li
"""

所属分组
    反向交割 API 测试
用例标题
    获取计划委托历史委托
前置条件

步骤/文本
    1.调用接口：api/v1/contract_trigger_hisorders
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
@allure.story('获取计划委托历史委托')  # 这里填子功能，没有的话就把本行注释掉
@allure.tag('Script owner : Alex Li', 'Case owner : Alex Li')
@pytest.mark.stable
class TestApiSchema_053:

    @allure.step('前置条件')
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, symbol):
        print("前置条件 {}".format(symbol))
        print(ATP.make_market_depth())
        # 切回持仓倍数
        res = contract_api.contract_switch_lever_rate(
            symbol="BTC", lever_rate=5)
        print(res)

    @allure.title('获取计划委托历史委托')
    @allure.step('测试执行')
    def test_execute(self, sub_uid):
        with allure.step('1、调用接口：api/v1/contract_trigger_hisorders'):
            pass
        with allure.step('2、接口返回的json格式、字段名、字段值正确'):
            # 构造持仓量
            price = ATP.get_current_price()
            common_contract_api.contract_order(
                symbol="BTC", contract_type="this_week", price=price, volume=5, direction="sell", offset="open")
            res_sell = contract_api.contract_trigger_order(
                symbol="BTC", contract_type="this_week", trigger_type="ge", trigger_price=price, order_price=price+1, volume=1, direction="buy", offset="open", lever_rate=5)
            print(res_sell)
            res = contract_api.contract_trigger_hisorders(
                symbol="BTC", trade_type=0, status=0, create_date=30)
            print(res)
            assert res['status'] == 'ok'
            assert common.util.compare_dictkey(
                ["symbol", "contract_code", "contract_type", "trigger_type", "volume", "order_type", "direction", "offset", "lever_rate",
                 "order_id", "order_id_str", "relation_order_id", "order_price_type", "status", "order_source", "trigger_price", "triggered_price", "order_price", "created_at", "triggered_at", "order_insert_at",
                 "update_time", "canceled_at", "fail_code", "fail_reason"], res["data"]["orders"][0])

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')
        print(ATP.clean_market())
        print(ATP.cancel_all_order())


if __name__ == '__main__':
    pytest.main()
