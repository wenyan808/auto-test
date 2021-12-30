#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20211229
# @Author : 
    用例标题
        全部入参大小写兼容测试
    前置条件
        
    步骤/文本
        1、调用linear-swap-api/v1/swap_contract_info接口，所有参数都用大小写混合的方式，检查系统响应有结果A)
    预期结果
        A)返回正常，无报错
    优先级
        1
    用例别名
        Test_api_linear_swap_contract_info_029
"""

from common.LinearServiceAPI import t as linear_api

from pprint import pprint
import pytest, allure, random, time


@allure.epic('正向永续')  # 这里填业务线
@allure.feature('API参数测试')  # 这里填功能
@allure.story('swap_contract_info接口')  # 这里填子功能，没有的话就把本行注释掉
@allure.tag('Script owner : 张广南', 'Case owner : 张广南')
@pytest.mark.stable
class Test_api_linear_swap_contract_info_029:

    @allure.step('前置条件')
    def setup(self):
        print('''  ''')

    @allure.title('全部入参大小写兼容测试')
    @allure.step('测试执行')
    def test_execute(self, contract_code):
        with allure.step('调用linear-swap-api/v1/swap_contract_info接口，所有参数都用大小写混合的方式，检查系统响应有结果A'):
            r = linear_api.linear_contract_info(contract_code=contract_code.capitalize(),
                                                support_margin_mode='ALL',
                                                business_type='swaP',
                                                pair=contract_code.lower(),
                                                contract_type='sWap')
            pprint(r)

            assert r['status'] == 'ok'

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')


if __name__ == '__main__':
    pytest.main()
