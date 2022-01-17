#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20211122
# @Author : 
    用例标题
        获取风险准备金历史数据（全逐通用）
    前置条件
        
    步骤/文本
        调用接口：/linear-swap-api/v1/swap_insurance_fund
    预期结果
        A)接口返回的json格式、字段名、字段值正确
    优先级
        0
    用例别名
        TestLinearApiSchema_006
"""

from common.LinearServiceAPI import t as linear_api

from pprint import pprint
from schema import Schema,Or
import pytest, allure, random, time


@allure.epic('正向永续')  # 这里填业务线
@allure.feature('api')  # 这里填功能
@allure.story('schema校验')  # 这里填子功能，没有的话就把本行注释掉
@allure.tag('Script owner : 张广南', 'Case owner : 张让翰')
@pytest.mark.stable
class TestLinearApiSchema_006:

    @allure.step('前置条件')
    def setup(self):
        print('''  ''')

    @allure.title('获取风险准备金历史数据（全逐通用）')
    @allure.step('测试执行')
    def test_execute(self, contract_code,symbol):
        with allure.step('调用接口：/linear-swap-api/v1/swap_insurance_fund'):
            trade_partition = linear_api.get_trade_partition(contract_code)
            r = linear_api.linear_insurance_fund(contract_code=contract_code, page_size='', page_index='')
            pprint(r)
            schema = {
                'data': {
                    'symbol': symbol,
                    'contract_code': contract_code,
                    'business_type': 'swap',
                    'pair': contract_code,
                    'trade_partition': trade_partition,
                    'tick': [
                        {
                            'insurance_fund': Or(float, 0),
                            'ts': int
                        }
                    ],
                    'current_page': int,
                    'total_page': int,
                    'total_size': int
                },
                'status': 'ok',
                'ts': int
            }

            Schema(schema).validate(r)

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')


if __name__ == '__main__':
    pytest.main()
