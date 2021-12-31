#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20211229
# @Author : 
    用例标题
        仅不填business_type参数测试
    前置条件
        
    步骤/文本
        1、调用linear-swap-api/v1/swap_contract_info接口，仅不传business参数，记录返回值。
        2、再次调用此接口，传business参数为'swap',对比第1步的返回值，有结果A
    预期结果
        A)两次返回值data里内容一致
    优先级
        1
    用例别名
        Test_api_linear_swap_contract_info_002
"""

from common.LinearServiceAPI import t as linear_api

from pprint import pprint
import pytest, allure, random, time


@allure.epic('正向永续')  # 这里填业务线
@allure.feature('API参数测试')  # 这里填功能
@allure.story('swap_contract_info接口')  # 这里填子功能，没有的话就把本行注释掉
@allure.tag('Script owner : 张广南', 'Case owner : 张广南')
@pytest.mark.stable
class Test_api_linear_swap_contract_info_002:

    @allure.step('前置条件')
    def setup(self):
        print('''  ''')

    @allure.title('仅不填business_type参数测试')
    @allure.step('测试执行')
    def test_execute(self, contract_code):
        with allure.step('1、调用linear-swap-api/v1/swap_contract_info接口，仅不传business参数，记录返回值。'):
            r1 = linear_api.linear_contract_info(contract_code=contract_code,
                                                 support_margin_mode='all',
                                                 business_type='',
                                                 pair='BTC-USDT',
                                                 contract_type='swap')
            pprint(r1)
        with allure.step('2、再次调用此接口，传business参数为swap,对比第1步的返回值，有结果A'):
            r2 = linear_api.linear_contract_info(contract_code=contract_code,
                                                 support_margin_mode='all',
                                                 business_type='swap',
                                                 pair='BTC-USDT',
                                                 contract_type='swap')
            pprint(r2)

            assert r1['data'] == r2['data']

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')


if __name__ == '__main__':
    pytest.main()
