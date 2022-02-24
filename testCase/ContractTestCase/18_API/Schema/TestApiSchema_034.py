#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/11/22
# @Author  : Alex Li
"""

所属分组
    反向交割 API 测试
用例标题
    获取用户API指标禁用信息
前置条件

步骤/文本
    1.调用接口：api/v1/contract_api_trading_status
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
@allure.story('获取用户API指标禁用信息')  # 这里填子功能，没有的话就把本行注释掉
@allure.tag('Script owner : Alex Li', 'Case owner : Alex Li')
@pytest.mark.stable
class TestApiSchema_034:

    @allure.step('前置条件')
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, symbol):
        print("前置条件 {}".format(symbol))

    @allure.title('获取用户API指标禁用信息')
    @allure.step('测试执行')
    def test_execute(self):
        with allure.step('1、调用接口：api/v1/contract_api_trading_status'):
            pass
        with allure.step('2、接口返回的json格式、字段名、字段值正确'):
            # 构造持仓量
            res = contract_api.contract_api_trading_status()
            pprint(res)

            schema = {"data": {"is_disable": int,
                               "order_price_types": str,
                               "disable_reason": str,
                               "disable_interval": int,
                               "recovery_time": int,
                               "COR": {"orders_threshold": int,
                                       "orders": int,
                                       "invalid_cancel_orders": int,
                                       "cancel_ratio_threshold": Or(float, int),
                                       "cancel_ratio": Or(float, int),
                                       "is_trigger": int,
                                       "is_active": int},
                               "TDN": {"disables_threshold": int,
                                       "disables": int,
                                       "is_trigger": int,
                                       "is_active": int}
                               },
                      "status": "ok",
                      "ts": int}
            Schema(schema).validate(res)

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')


if __name__ == '__main__':
    pytest.main()
