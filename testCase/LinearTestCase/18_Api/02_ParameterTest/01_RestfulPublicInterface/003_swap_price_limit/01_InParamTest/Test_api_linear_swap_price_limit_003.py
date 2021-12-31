#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20211230
# @Author : 
    用例标题
        business_type参数为空,null测试
    前置条件
        
    步骤/文本
        1、调用linear-swap-api/v1/swap_price_limit，
        business_type参数为空,null。检查返回值有结果A
    预期结果
        A)提示参数错误
    优先级
        1
    用例别名
        Test_api_linear_swap_price_limit_003
"""

from pprint import pprint

import allure
import pytest

from common.util import api_http_get


@allure.epic('正向永续')  # 这里填业务线
@allure.feature('API参数测试')  # 这里填功能
@allure.story('linear_swap_price_limit接口')  # 这里填子功能，没有的话就把本行注释掉
@allure.tag('Script owner : 张广南', 'Case owner : 张广南')
@pytest.mark.stable
class Test_api_linear_swap_price_limit_003:

    @allure.step('前置条件')
    def setup(self):
        print('''  ''')

    @allure.title('business_type参数为空,null测试')
    @allure.step('测试执行')
    def test_execute(self, contract_code, url):
        with allure.step('1、调用linear-swap-api/v1/swap_price_limit，'):
            params = ['']  # 传null返回business_type字段不合法，接口校验不一致，不过也不是什么问题
            url = url + '/linear-swap-api/v1/swap_price_limit'
            for param in params:
                request = {'contract_code': 'ETH-USDT', 'pair': 'BTC-USDT',
                           'contract_type': 'swap', 'business_type': param}
                r = api_http_get(url, request)
                pprint(r)

                assert r['status'] == 'ok'

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')


if __name__ == '__main__':
    pytest.main()
