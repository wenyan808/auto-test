#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/11/22
# @Author  : Alex Li
"""

所属分组
    反向交割 API 测试
用例标题
    获取计划委托当前委托
前置条件

步骤/文本
    1.调用接口：api/v1/contract_trigger_openorders
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
@allure.story('获取计划委托当前委托')  # 这里填子功能，没有的话就把本行注释掉
@allure.tag('Script owner : Alex Li', 'Case owner : Alex Li')
@pytest.mark.stable
class TestApiSchema_052:

    @allure.step('前置条件')
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, symbol):
        print("前置条件 {}".format(symbol))
        self.buyprice = ATP.get_adjust_price(rate=0.98)

    @allure.title('获取计划委托当前委托')
    @allure.step('测试执行')
    def test_execute(self, symbol, symbol_period):
        with allure.step('1、调用接口：api/v1/contract_trigger_openorders'):
            pass
        with allure.step('2、接口返回的json格式、字段名、字段值正确'):
            # 构造持仓量
            contract_type = get_contract_type(symbol_period)
            contract_api.contract_trigger_order(symbol=symbol,
                                                contract_type=contract_type,
                                                trigger_type="le",
                                                trigger_price=self.buyprice,
                                                order_price=self.buyprice,
                                                volume=1,
                                                direction="buy",
                                                offset="open",
                                                lever_rate=5)

            time.sleep(2)
            res = contract_api.contract_trigger_openorders(symbol=symbol)
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
                            "order_type": Or(float, int),
                            "direction": str,
                            "offset": str,
                            "lever_rate": Or(float, int),
                            "order_id": int,
                            "order_id_str": str,
                            "order_source": str,
                            "trigger_price": Or(float, int),
                            "order_price": Or(float, int),
                            "created_at": int,
                            "order_price_type": str,
                            "status": int,
                            'update_time': int
                        }
                    ],
                    "total_page": int,
                    "current_page": int,
                    "total_size": int
                },
                "ts": int
            }
            #assert res['data']['orders']
            Schema(schema).validate(res)

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')
       # print(ATP.cancel_all_trigger_order())


if __name__ == '__main__':
    pytest.main()
