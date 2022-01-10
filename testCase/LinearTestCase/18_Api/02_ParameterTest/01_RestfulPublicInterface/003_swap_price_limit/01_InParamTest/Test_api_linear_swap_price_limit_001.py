#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20211230
# @Author : 
    用例标题
        所有非必填参数都不填测试
    前置条件
        
    步骤/文本
        1、调用linear-swap-api/v1/swap_price_limit，所有非必填参数都不填。检查返回值有结果A
    预期结果
        A)返回状态为OK，并且data不为空
    优先级
        1
    用例别名
        Test_api_linear_swap_price_limit_001
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
class Test_api_linear_swap_price_limit_001:

    @allure.step('前置条件')
    def setup(self):
        print('''  ''')

    @allure.title('所有非必填参数都不填测试')
    @allure.step('测试执行')
    def test_execute(self, contract_code):
        with allure.step('1、调用linear-swap-api/v1/swap_price_limit，所有非必填参数都不填。检查返回值有结果A'):
            r = linear_api.linear_price_limit()
            pprint(r)

            assert r['status'] == 'ok'
            assert len(r['data']) > 1


    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')


if __name__ == '__main__':
    pytest.main()
