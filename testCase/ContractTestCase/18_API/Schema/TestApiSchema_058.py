#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/11/22
# @Author  : Alex Li
"""

所属分组
    反向交割 API 测试
用例标题
    获取止盈止损历史委托
前置条件

步骤/文本
    1.调用接口：api/v1/contract_tpsl_hisorders
预期结果
    A)接口返回的json格式、字段名、字段值正确
优先级
    1
"""
import time
from pprint import pprint

import allure
import pytest
from schema import Schema, Or

from common.ContractServiceAPI import t as contract_api
from common.util import get_contract_type
from tool.atp import ATP


@allure.epic('反向交割')  # 这里填业务线
@allure.feature('API 测试')  # 这里填功能
@allure.story('获取止盈止损历史委托')  # 这里填子功能，没有的话就把本行注释掉
@allure.tag('Script owner : Alex Li', 'Case owner : Alex Li')
@pytest.mark.stable
class TestApiSchema_058:

    @allure.step('前置条件')
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, symbol):
        print("前置条件 {}".format(symbol))

    @allure.title('获取止盈止损历史委托')
    @allure.step('测试执行')
    def test_execute(self, symbol):
        with allure.step('1、调用接口：api/v1/contract_tpsl_hisorders'):
            pass
        with allure.step('2、接口返回的json格式、字段名、字段值正确'):
            # 构造持仓量

            res = contract_api.contract_tpsl_hisorders(symbol=symbol, status=0, create_date=30)
            pprint(res)

            schema = {"data": {"orders": [{"symbol": str,
                                           "contract_code": str,
                                           "contract_type": str,
                                           "volume": Or(float, int),
                                           "order_type": int,
                                           "tpsl_order_type": str,
                                           "direction": str,
                                           "order_id": int,
                                           "order_id_str": str,
                                           "order_source": str,
                                           "trigger_type": str,
                                           "trigger_price": Or(float, int),
                                           "order_price": Or(float, int),
                                           "created_at": int,
                                           "order_price_type": str,
                                           "status": int,
                                           "source_order_id": Or(str, int, None),
                                           "relation_tpsl_order_id": str,
                                           "canceled_at": int,
                                           "fail_code": Or(float, int, None),
                                           "fail_reason": Or(float, int, None),
                                           "triggered_price": Or(float, int, None),
                                           "relation_order_id": str,
                                           "update_time": int}],
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
