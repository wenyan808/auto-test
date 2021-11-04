#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20211019
# @Author : 
    用例标题
        WS订阅成交(sub)  合约结算中
    前置条件
        
    步骤/文本
        详见官方文档
    预期结果
        
    优先级
        3
    用例别名
        TestContractNoti_ws_trade_013
"""

from common.ContractServiceAPI import t as contract_api
from common.ContractServiceOrder import t as contract_order
from common.LinearServiceAPI import t as linear_api
from common.LinearServiceOrder import t as linear_order
from common.SwapServiceAPI import t as swap_api
from common.SwapServiceOrder import t as swap_order

from pprint import pprint
import pytest, allure, random, time


@allure.epic('业务线')  # 这里填业务线
@allure.feature('功能')  # 这里填功能
@allure.story('子功能')  # 这里填子功能，没有的话就把本行注释掉
class TestContractNoti_ws_trade_013:

    @allure.step('前置条件')
    def setup(self):
        print('''  ''')

    @allure.title('WS订阅成交(sub)  合约结算中')
    @allure.step('测试执行')
    def test_execute(self, symbol, symbol_period):
        with allure.step('详见官方文档'):
            pass#暂无法构造结算场景

    @allure.step('恢复环境')
    def teardown(self):
        ATP.clean_market()
        ATP.cancel_all_order()


if __name__ == '__main__':
    pytest.main()
