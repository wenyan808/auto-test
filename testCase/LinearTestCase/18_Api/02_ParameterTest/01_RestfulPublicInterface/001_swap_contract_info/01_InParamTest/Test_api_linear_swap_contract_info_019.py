#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20211229
# @Author : 
    用例标题
        contract_code参数在取值范围内测试
    前置条件
        
    步骤/文本
        1、调用linear-swap-api/v1/swap_contract_info接口，contract_code参数在取值范围内。检查返回值有结果A
    预期结果
        A)
    优先级
        1
    用例别名
        Test_api_linear_swap_contract_info_019
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
class Test_api_linear_swap_contract_info_019:

    @allure.step('前置条件')
    def setup(self):
        print('''  ''')

    @allure.title('contract_code参数在取值范围内测试')
    @allure.step('测试执行')
    def test_execute(self, symbol, symbol_period):
        with allure.step('1、调用linear-swap-api/v1/swap_contract_info接口，contract_code参数在取值范围内。检查返回值有结果A'):
            pass

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')


if __name__ == '__main__':
    pytest.main()
