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
from pprint import pprint

import allure
import common.util
import pytest
from common.ContractServiceAPI import common_user_contract_service_api as common_contract_api
from common.ContractServiceAPI import t as contract_api
from schema import Or, Schema
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

    @allure.title('获取计划委托历史委托')
    @allure.step('测试执行')
    def test_execute(self, symbol):
        with allure.step('1、调用接口：api/v1/contract_trigger_hisorders'):
            pass
        with allure.step('2、接口返回的json格式、字段名、字段值正确'):
            # 构造持仓量
            res = contract_api.contract_trigger_hisorders(
                symbol=symbol, trade_type=0, status=0, create_date=30)
            pprint(res)
            schema = {
                "status": "ok",
                "data": {
                    "orders": [
                        {
                            "symbol": str,
                            "contract_code": str,
                            "contract_type": str,
                            "trigger_type": str,
                            "volume": Or(float, int),
                            "order_type": int,
                            "direction": str,
                            "offset": str,
                            "lever_rate": Or(float, int),
                            "order_id": int,
                            "order_id_str": str,
                            "relation_order_id": str,
                            "order_price_type": str,
                            "status": int,
                            "order_source": str,
                            "trigger_price": Or(float, int),
                            "triggered_price": Or(float, int, None),
                            "order_price": Or(float, int),
                            "created_at": int,
                            "triggered_at": Or(float, int, None),
                            "order_insert_at": int,
                            "update_time": int,
                            "canceled_at": int,
                            "fail_code": Or(float, int, None),
                            "fail_reason": Or(str, None)
                        }
                    ],
                    "total_page": int,
                    "current_page": int,
                    "total_size": int
                },
                "ts": int
            }
            Schema(schema).validate(res)

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')


if __name__ == '__main__':
    pytest.main()
