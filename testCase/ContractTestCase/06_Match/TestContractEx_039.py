#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20211021
# @Author : 
    用例标题
        撮合当周 最优5档IOC 买入 平仓            
    前置条件
        
    步骤/文本
        详见官方文档
    预期结果
        正确撮合
    优先级
        2
    用例别名
        TestContractEx_039
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
class TestContractEx_039:

    @allure.step('前置条件')
    def setup(self):
        print('''  ''')

    @allure.title('撮合当周 最优5档IOC 买入 平仓            ')
    @allure.step('测试执行')
    def test_execute(self, symbol, symbol_period):
        with allure.step('详见官方文档'):
            pass

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')


if __name__ == '__main__':
    pytest.main()
