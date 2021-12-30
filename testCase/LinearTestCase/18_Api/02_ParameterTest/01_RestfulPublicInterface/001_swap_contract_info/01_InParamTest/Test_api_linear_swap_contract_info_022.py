#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20211229
# @Author : 
    用例标题
        contract_code参数优先级最高测试
    前置条件
        
    步骤/文本
        1、调用linear-swap-api/v1/swap_contract_info接口，同时填写pair、contract_type和contract_code，但pair、contract_type和contract_code矛盾。记录返回值。
        2、在第1步的传参基础上去掉contract_code，对比第1步的返回值有结果A
        3、在第1步的传参基础上去掉pair、contract_type，对比第1步的返回值有结果B
    预期结果
        A)两次返回值data里内容不一致
        B)两次返回值data里内容一致
    优先级
        1
    用例别名
        Test_api_linear_swap_contract_info_022
"""

from common.LinearServiceAPI import t as linear_api

from pprint import pprint
import pytest, allure, random, time


@allure.epic('正向永续')  # 这里填业务线
@allure.feature('API参数测试')  # 这里填功能
@allure.story('swap_contract_info接口')  # 这里填子功能，没有的话就把本行注释掉
@allure.tag('Script owner : 张广南', 'Case owner : 张广南')
@pytest.mark.stable
class Test_api_linear_swap_contract_info_022:

    @allure.step('前置条件')
    def setup(self):
        print('''  ''')

    @allure.title('contract_code参数优先级最高测试')
    @allure.step('测试执行')
    def test_execute(self):
        with allure.step(
                '1、调用linear-swap-api/v1/swap_contract_info接口，同时填写pair、contract_type和contract_code，但pair、contract_type和contract_code矛盾。记录返回值。'):
            r = linear_api.linear_contract_info()
            pprint(r)
            contract_code0 = r['data'][0]['contract_code']
            pair1 = r['data'][1]['pair']
            contract_type1 = r['data'][1]['contract_type']

            r1 = linear_api.linear_contract_info(contract_code=contract_code0,
                                                 support_margin_mode='',
                                                 business_type='',
                                                 pair=pair1,
                                                 contract_type=contract_type1)
            pprint(r1)

        with allure.step('2、在第1步的传参基础上去掉contract_code，对比第1步的返回值有结果A'):
            r2 = linear_api.linear_contract_info(contract_code='',
                                                 support_margin_mode='',
                                                 business_type='',
                                                 pair=pair1,
                                                 contract_type=contract_type1)
            pprint(r2)
            assert r2['data'] != r1['data']
        with allure.step('3、在第1步的传参基础上去掉pair、contract_type，对比第1步的返回值有结果B'):
            r3 = linear_api.linear_contract_info(contract_code=contract_code0,
                                                 support_margin_mode='',
                                                 business_type='',
                                                 pair='',
                                                 contract_type='')
            pprint(r3)
            assert r3['data'] == r1['data']
            # for i in r['data']:
            #     contract_code = i['contract_code']
            #     r1 = linear_api.linear_contract_info(contract_code=contract_code,
            #                                          support_margin_mode='',
            #                                          business_type='',
            #                                          pair='',
            #                                          contract_type='')
            #     pprint(r1)
            #
            #     assert r1['data'][0]['pair'] == contract_code
            #     assert len(r1['data']) == 1

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')


if __name__ == '__main__':
    pytest.main()
