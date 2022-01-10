#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20211229
# @Author : 
    用例标题
        contract_code参数为特殊字符测试
    前置条件
        
    步骤/文本
        1、调用linear-swap-api/v1/swap_contract_info接口，contract_code参数为特殊字符。检查返回值有结果A
    预期结果
        A)提示参数错误
    优先级
        1
    用例别名
        Test_api_linear_swap_contract_info_021
"""

from pprint import pprint

import allure
import pytest

from common.LinearServiceAPI import t as linear_api


@allure.epic('正向永续')  # 这里填业务线
@allure.feature('API参数测试')  # 这里填功能
@allure.story('swap_contract_info接口')  # 这里填子功能，没有的话就把本行注释掉
@allure.tag('Script owner : 张广南', 'Case owner : 张广南')
@pytest.mark.stable
class Test_api_linear_swap_contract_info_021:

    @allure.step('前置条件')
    def setup(self):
        print('''  ''')

    @allure.title('contract_code参数为特殊字符测试')
    @allure.step('测试执行')
    def test_execute(self):
        with allure.step('1、调用linear-swap-api/v1/swap_contract_info接口，contract_code参数为特殊字符。检查返回值有结果A'):
            paralist = ['#', '!', '%', '*', '&', '.', '$', '#^%$&%*^()*(@$!']

            for i in range(len(paralist)):
                r = linear_api.linear_contract_info(contract_code=paralist[i],
                                                    support_margin_mode='',
                                                    business_type='',
                                                    pair='',
                                                    contract_type='')
                pprint(r)
                assert r['status'] == 'error'
                assert r['err_msg'] == '合约不存在'

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')


if __name__ == '__main__':
    pytest.main()
