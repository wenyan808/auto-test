#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20211122
# @Author : 
    用例标题
        获取母账户下的所有母子账户划转记录（全逐通用）
    前置条件
        
    步骤/文本
        调用接口：/linear-swap-api/v1/swap_master_sub_transfer_record
    预期结果
        A)接口返回的json格式、字段名、字段值正确
    优先级
        0
    用例别名
        TestLinearApiSchema_040
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
class TestLinearApiSchema_040:

    @allure.step('前置条件')
    def setup(self):
        print('''  ''')

    @allure.title('获取母账户下的所有母子账户划转记录（全逐通用）')
    @allure.step('测试执行')
    def test_execute(self, contract_code, symbol):
        with allure.step('调用接口：/linear-swap-api/v1/swap_master_sub_transfer_record'):
            r = linear_api.linear_master_sub_transfer_record(margin_account=contract_code,
                                                    transfer_type='34',
                                                    create_date='7',
                                                    page_index='',
                                                    page_size='')
            pprint(r)
            schema = {
                'data': {
                    'current_page': int,
                    'total_page': int,
                    'total_size': int,
                    'transfer_record': [
                        {
                            'amount': float,
                            'asset': 'USDT',
                            'from_margin_account': str,
                            'id': int,
                            'margin_account': str,
                            'sub_account_name': str,
                            'sub_uid': str,
                            'to_margin_account': str,
                            'transfer_type': int,
                            'ts': int
                        }
                    ]
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
