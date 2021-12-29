#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20211229
# @Author : 
    用例标题
        business_type参数为特殊字符测试
    前置条件
        
    步骤/文本
        1、调用linear-swap-api/v1/swap_contract_info接口，business_type参数为特殊字符。检查返回值有结果A
    预期结果
        A)提示参数错误
    优先级
        1
    用例别名
        Test_api_linear_swap_contract_info_006
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
class Test_api_linear_swap_contract_info_006:

    @allure.step('前置条件')
    def setup(self):
        print('''  ''')

    @allure.title('business_type参数为特殊字符测试')
    @allure.step('测试执行')
    def test_execute(self, symbol, symbol_period):
        with allure.step('1、调用linear-swap-api/v1/swap_contract_info接口，business_type参数为特殊字符。检查返回值有结果A'):
            paralist = ['swapp', 'contract', 'linear']

            for i in range(len(paralist)):
                r = linear_api.linear_contract_info(contract_code='',
                                                    support_margin_mode='all',
                                                    business_type=paralist[i],
                                                    pair='',
                                                    contract_type='swap')
                pprint(r)
                assert r['status'] == 'error'
                assert r['err_msg'] == 'business_type字段不合法'

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')


if __name__ == '__main__':
    pytest.main()
