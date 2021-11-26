#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/11/22
# @Author  : Alex Li
"""

所属分组
    反向交割 API 测试
用例标题
    获取合约最高限价和最低限价
前置条件

步骤/文本
    1.调用接口：api /v1/contract_price_limit
预期结果
    A)接口返回的json格式、字段名、字段值正确
优先级
    1
"""


import allure
import common.util
import pytest
from common.ContractServiceAPI import t as contract_api


@allure.epic('反向交割')  # 这里填业务线
@allure.feature('API 测试')  # 这里填功能
@allure.story('获取合约最高限价和最低限价')  # 这里填子功能，没有的话就把本行注释掉
@allure.tag('Script owner : Alex Li', 'Case owner : Alex Li')
@pytest.mark.stable
class TestApiSchema_003:

    @allure.step('前置条件')
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, symbol):
        print("前置条件 {}".format(symbol))

    @allure.title('获取合约最高限价和最低限价')
    @allure.step('测试执行')
    def test_execute(self):
        with allure.step('1、调用接口：api /v1/contract_price_limit'):
            pass
        with allure.step('2、接口返回的json格式、字段名、字段值正确'):
            res = contract_api.contract_price_limit(
                symbol='BTC', contract_type="this_week")
            print(res)
            assert res['status'] == 'ok'
            assert common.util.compare_dictkey(
                ["symbol", "index_price", "contract_type", "high_limit", "low_limit"], res.data[0])

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')


if __name__ == '__main__':
    pytest.main()
