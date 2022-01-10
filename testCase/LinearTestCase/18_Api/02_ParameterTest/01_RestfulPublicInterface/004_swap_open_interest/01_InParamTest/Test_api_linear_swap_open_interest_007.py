#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20211231
# @Author : 
    用例标题
        仅不填pair参数测试
    前置条件
        
    步骤/文本
        1、调用linear-swap-api/v1/swap_open_interest接口，仅不填pair参数。检查返回值有结果A
    预期结果
        A)
    优先级
        1
    用例别名
        Test_api_linear_swap_open_interest_007
"""

from common.LinearServiceAPI import t as linear_api

from pprint import pprint
import pytest, allure, random, time


@allure.epic('正向永续')  # 这里填业务线
@allure.feature('API参数测试')  # 这里填功能
@allure.story('swap_open_interest')  # 这里填子功能，没有的话就把本行注释掉
@allure.tag('Script owner : 张广南', 'Case owner : 张广南')
@pytest.mark.stable
class Test_api_linear_swap_open_interest_007:

    @allure.step('前置条件')
    def setup(self):
        print('''  ''')

    @allure.title('仅不填pair参数测试')
    @allure.step('测试执行')
    def test_execute(self, contract_code):
        with allure.step('1、调用linear-swap-api/v1/swap_open_interest接口，仅不填pair参数。检查返回值有结果A'):
            r = linear_api.linear_open_interest(contract_code='',#由于contract_code有更高优先级，因此此用例不传contract_code
                                                business_type='swap',
                                                pair='',
                                                contract_type='swap')
            pprint(r)
            assert r['status'] == 'ok'
            assert len(r['data']) > 1

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')


if __name__ == '__main__':
    pytest.main()
