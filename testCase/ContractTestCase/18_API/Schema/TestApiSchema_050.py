#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/11/22
# @Author  : Alex Li
"""

所属分组
    反向交割 API 测试
用例标题
    合约计划委托撤单
前置条件

步骤/文本
    1.调用接口：api/v1/contract_trigger_cancel
预期结果
    A)接口返回的json格式、字段名、字段值正确
优先级
    1
"""

import allure
import pytest
from schema import Schema

from common.ContractServiceAPI import t as contract_api
from common.util import get_contract_type
from tool.atp import ATP


@allure.epic('反向交割')  # 这里填业务线
@allure.feature('API 测试')  # 这里填功能
@allure.story('合约计划委托撤单')  # 这里填子功能，没有的话就把本行注释掉
@allure.tag('Script owner : Alex Li', 'Case owner : Alex Li')
@pytest.mark.stable
class TestApiSchema_050:

    @allure.step('前置条件')
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, symbol):
        print("前置条件 {}".format(symbol))
        self.buyprice = ATP.get_adjust_price(rate=0.98)

    @allure.title('合约计划委托撤单')
    @allure.step('测试执行')
    def test_execute(self, symbol, symbol_period):
        with allure.step('1、调用接口：api/v1/contract_trigger_cancel'):
            pass
        with allure.step('2、接口返回的json格式、字段名、字段值正确'):
            # 构造持仓量
            contract_type = get_contract_type(symbol_period)
            res_sell = contract_api.contract_trigger_order(symbol=symbol,
                                                           contract_type=contract_type,
                                                           trigger_type="le",
                                                           trigger_price=self.buyprice,
                                                           order_price=self.buyprice,
                                                           volume=1,
                                                           direction="buy",
                                                           offset="open",
                                                           lever_rate=5)
            res = contract_api.contract_trigger_cancel(
                symbol=symbol, order_id=res_sell["data"]["order_id_str"])
            print(res)

            schema = {"data": {"errors": [{"order_id": str,
                                           "err_code": int,
                                           "err_msg": str}],
                               "successes": str
                               },
                      "status": "ok",
                      "ts": int
                      }
            Schema(schema).validate(res)

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')


if __name__ == '__main__':
    pytest.main()
