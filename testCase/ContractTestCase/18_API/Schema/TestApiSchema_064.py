#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/11/22
# @Author  : Alex Li
"""

所属分组
    反向交割 API 测试
用例标题
    获取跟踪委托历史委托
前置条件

步骤/文本
    1.调用接口：api/v1/contract_track_hisorders
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
@allure.story('获取跟踪委托历史委托')  # 这里填子功能，没有的话就把本行注释掉
@allure.tag('Script owner : Alex Li', 'Case owner : Alex Li')
@pytest.mark.stable
class TestApiSchema_063:

    @allure.step('前置条件')
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, symbol):
        print("前置条件 {}".format(symbol))

    @allure.title('获取跟踪委托历史委托')
    @allure.step('测试执行')
    def test_execute(self, symbol, symbol_period):
        with allure.step('1、调用接口：api/v1/contract_track_hisorders'):
            pass
        with allure.step('2、接口返回的json格式、字段名、字段值正确'):
            res = contract_api.contract_track_hisorders(symbol=symbol,
                                                        trade_type=0,
                                                        status=0,
                                                        create_date=30)
            pprint(res)

            schema = {"data": {"orders": [{"symbol": str,
                                           "contract_type": str,
                                           "contract_code": str,
                                           "triggered_price": Or(float, int, None),
                                           "volume": Or(float, int),
                                           "order_type": int,
                                           "direction": str,
                                           "offset": str,
                                           "lever_rate": Or(float, int),
                                           "order_id": int,
                                           "order_id_str": str,
                                           "order_source": str,
                                           "created_at": int,
                                           "update_time": int,
                                           "order_price_type": str,
                                           "status": int,
                                           "canceled_at": int,
                                           "fail_code": Or(int, None),
                                           "fail_reason": Or(str, None),
                                           "callback_rate": Or(float, int),
                                           "active_price": Or(float, int),
                                           "is_active": int,
                                           "market_limit_price": Or(float, int, None),
                                           "formula_price": Or(float, int, None),
                                           "real_volume": Or(float, int),
                                           "relation_order_id": str}],
                               "total_page": int,
                               "current_page": int,
                               "total_size": int},
                      "status": "ok",
                      "ts": int}
            Schema(schema).validate(res)

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')


if __name__ == '__main__':
    pytest.main()
