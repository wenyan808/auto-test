#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20211122
# @Author : 
    用例标题
        查询母账户下所有子账户资产信息（逐仓）
    前置条件
        
    步骤/文本
        调用接口：/linear-swap-api/v1/swap_sub_account_list
    预期结果
        A)接口返回的json格式、字段名、字段值正确
    优先级
        0
    用例别名
        TestLinearApiSchema_027
"""

from pprint import pprint

import allure
import pytest
from schema import Schema, Or

from common.LinearServiceAPI import t as linear_api


@allure.epic('正向永续')  # 这里填业务线
@allure.feature('api')  # 这里填功能
@allure.story('schema校验')  # 这里填子功能，没有的话就把本行注释掉
@allure.tag('Script owner : 张广南', 'Case owner : 张让翰')
@pytest.mark.stable
class TestLinearApiSchema_027:

    @allure.step('前置条件')
    def setup(self):
        print('''  ''')

    @allure.title('查询母账户下所有子账户资产信息（逐仓）')
    @allure.step('测试执行')
    def test_execute(self, contract_code, symbol):
        with allure.step('调用接口：/linear-swap-api/v1/swap_sub_account_list'):
            r = linear_api.linear_sub_account_list(contract_code=contract_code)
            pprint(r)
            schema = {
                'data': [
                    {
                        'list': [
                            {
                                'contract_code': contract_code,
                                'liquidation_price': Or(int, float, None),
                                'margin_account': str,
                                'margin_asset': 'USDT',
                                'margin_balance': Or(int, float, None),
                                'margin_mode': 'isolated',
                                'risk_rate': Or(int, float, None),
                                'symbol': symbol
                            }
                        ],
                        'sub_uid': int
                    }
                ],
                'status': 'ok',
                'ts': int
            }

            Schema(schema).validate(r)

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')


if __name__ == '__main__':
    pytest.main()
