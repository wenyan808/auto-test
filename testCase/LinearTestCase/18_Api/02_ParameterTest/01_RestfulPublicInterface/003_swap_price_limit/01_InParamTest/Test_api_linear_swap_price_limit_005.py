#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20211230
# @Author : 
    用例标题
        business_type参数在取值范围外测试
    前置条件
        
    步骤/文本
        1、调用linear-swap-api/v1/swap_price_limit，business_type参数在取值范围外。检查返回值有结果A
    预期结果
        A)提示参数错误
    优先级
        1
    用例别名
        Test_api_linear_swap_price_limit_005
"""

from pprint import pprint

import allure
import pytest

from common.LinearServiceAPI import t as linear_api


@allure.epic('正向永续')  # 这里填业务线
@allure.feature('API参数测试')  # 这里填功能
@allure.story('linear_swap_price_limit')  # 这里填子功能，没有的话就把本行注释掉
@allure.tag('Script owner : 张广南', 'Case owner : 张广南')
@pytest.mark.stable
class Test_api_linear_swap_price_limit_005:

    @allure.step('前置条件')
    def setup(self):
        print('''  ''')

    @allure.title('business_type参数在取值范围外测试')
    @allure.step('测试执行')
    def test_execute(self):
        with allure.step('1、调用linear-swap-api/v1/swap_price_limit，business_type参数在取值范围外。检查返回值有结果A'):
            paralist = ['swapp', 'contract', 'linear']
            for i in range(len(paralist)):
                r = linear_api.linear_price_limit(contract_code='',
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
