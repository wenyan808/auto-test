#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20211122
# @Author : 
    用例标题
        查询母账户下的单个子账户持仓信息（逐仓）
    前置条件
        
    步骤/文本
        调用接口：/linear-swap-api/v1/swap_sub_position_info
    预期结果
        A)接口返回的json格式、字段名、字段值正确
    优先级
        0
    用例别名
        TestLinearApiSchema_029
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
class TestLinearApiSchema_029:

    @allure.step('前置条件')
    def setup(self):
        print('''  ''')

    @allure.title('查询母账户下的单个子账户持仓信息（逐仓）')
    @allure.step('测试执行')
    def test_execute(self, contract_code, symbol):
        with allure.step('调用接口：/linear-swap-api/v1/swap_sub_position_info'):
            r = linear_api.linear_sub_account_list(contract_code=contract_code)
            subuid = r['data'][0]['sub_uid']
            trade_partition = linear_api.get_trade_partition(contract_code)
            r = linear_api.linear_sub_position_info(contract_code=contract_code, sub_uid=subuid)
            pprint(r)
            schema = {
                'data': [
                    {
                        'available': float,
                        'contract_code': contract_code,
                        'cost_hold': float,
                        'cost_open': float,
                        'direction': str,
                        'frozen': float,
                        'last_price': Or(float, int),
                        'lever_rate': int,
                        'margin_asset': trade_partition,
                        'margin_account': str,
                        'margin_mode': 'isolated',
                        'position_margin': float,
                        'profit': float,
                        'profit_rate': float,
                        'profit_unreal': float,
                        'symbol': symbol,
                        'volume': float,
                        'trade_partition': trade_partition,
                        'position_mode': Or('single_side', 'dual_side')
                    }
                ],
                'status': 'ok',
                'ts': int
            }
            assert r['data']
            Schema(schema).validate(r)

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')


if __name__ == '__main__':
    pytest.main()
