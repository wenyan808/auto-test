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

from common.LinearServiceAPI import t as linear_api

from pprint import pprint
import pytest, allure, random, time


@allure.epic('正向永续')  # 这里填业务线
@allure.feature('API参数测试')  # 这里填功能
@allure.story('swap_contract_info接口')  # 这里填子功能，没有的话就把本行注释掉
@allure.tag('Script owner : 张广南', 'Case owner : 张广南')
@pytest.mark.stable
class Test_api_linear_swap_contract_info_019:

    @allure.step('前置条件')
    def setup(self):
        print('''  ''')

    @allure.title('contract_code参数在取值范围内测试')
    @allure.step('测试执行')
    def test_execute(self):
        with allure.step('1、调用linear-swap-api/v1/swap_contract_info接口，contract_code参数在取值范围内。检查返回值有结果A'):
            r = linear_api.linear_contract_info()
            pprint(r)
            for i in r['data']:
                contract_code = i['contract_code']
                r1 = linear_api.linear_contract_info(contract_code=contract_code,
                                                     support_margin_mode='',
                                                     business_type='',
                                                     pair='',
                                                     contract_type='')
                pprint(r1)

                assert r1['data'][0]['pair'] == contract_code
                assert len(r1['data']) == 1

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')


if __name__ == '__main__':
    pytest.main()
