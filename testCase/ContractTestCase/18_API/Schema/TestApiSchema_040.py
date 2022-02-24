#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/11/22
# @Author  : Alex Li
"""

所属分组
    反向交割 API 测试
用例标题
    切换杠杆倍数
前置条件

步骤/文本
    1.调用接口：api/v1/contract_switch_lever_rate
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
@allure.story('切换杠杆倍数')  # 这里填子功能，没有的话就把本行注释掉
@allure.tag('Script owner : Alex Li', 'Case owner : Alex Li')
@pytest.mark.stable
class TestApiSchema_040:

    @allure.step('前置条件')
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, symbol):
        print("前置条件 {}".format(symbol))

    @allure.title('切换杠杆倍数')
    @allure.step('测试执行')
    def test_execute(self, symbol):
        with allure.step('1、调用接口：api/v1/contract_switch_lever_rate'):
            pass
        with allure.step('2、接口返回的json格式、字段名、字段值正确'):
            # 构造持仓量

            res = contract_api.contract_switch_lever_rate(symbol=symbol, lever_rate=1)
            print(res)
            schema = {
                "status": "ok",
                "data": {
                    "symbol": str,
                    "lever_rate": int
                },
                "ts": int
            }
            Schema(schema).validate(res)

    @allure.step('恢复环境')
    @pytest.fixture(scope='function', autouse=True)
    def teardown(self, symbol):
        contract_api.contract_switch_lever_rate(symbol=symbol, lever_rate=5)
        print('\n恢复环境操作')


if __name__ == '__main__':
    pytest.main()
