#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20211122
# @Author : 
    用例标题
        获取用户资产和持仓信息（逐仓）
    前置条件
        
    步骤/文本
        调用接口：/linear-swap-api/v1/swap_account_position_info
    预期结果
        A)接口返回的json格式、字段名、字段值正确
    优先级
        0
    用例别名
        TestLinearApiSchema_038
"""
import time
from pprint import pprint

import allure
import pytest
from schema import Schema, Or

from common.LinearServiceAPI import t as linear_api
from tool.atp import ATP


@allure.epic('正向永续')  # 这里填业务线
@allure.feature('api')  # 这里填功能
@allure.story('schema校验')  # 这里填子功能，没有的话就把本行注释掉
@allure.tag('Script owner : 张广南', 'Case owner : 张让翰')
@pytest.mark.stable
class TestLinearApiSchema_038:

    @allure.step('前置条件')
    def setup(self):
        print('''  ''')

    @allure.title('获取用户资产和持仓信息（逐仓）')
    @allure.step('测试执行')
    def test_execute(self, contract_code, symbol):
        with allure.step('调用接口：/linear-swap-api/v1/swap_account_position_info'):
            lastprice = ATP.get_current_price()

            sell_order = linear_api.linear_order(contract_code=contract_code,
                                                 price=lastprice,
                                                 volume='1',
                                                 direction='sell',
                                                 offset='open',
                                                 order_price_type="limit")
            pprint(sell_order)

            buy_order = linear_api.linear_order(contract_code=contract_code,
                                                price=lastprice,
                                                volume='1',
                                                direction='buy',
                                                offset='open',
                                                order_price_type="limit")
            pprint(buy_order)

            time.sleep(1)
            r = linear_api.linear_account_position_info(contract_code=contract_code)
            pprint(r)
            schema = {
                'data': [
                    {
                        'adjust_factor': Or(float, int),
                        'contract_code': contract_code,
                        'lever_rate': int,
                        'liquidation_price': Or(float, None),
                        'margin_account': str,
                        'margin_asset': 'USDT',
                        'margin_available': Or(float, None),
                        'margin_balance': Or(float, None),
                        'margin_frozen': Or(float, None, int),
                        'margin_mode': 'isolated',
                        'margin_position': Or(float, None),
                        'margin_static': Or(float, None),
                        'trade_partition': 'USDT',
                        'positions': Or([
                            {
                                'available': Or(float, None),
                                'contract_code': str,
                                'cost_hold': Or(float, None),
                                'cost_open': Or(float, None),
                                'direction': str,
                                'frozen': Or(float, None),
                                'last_price': Or(float, None, int),
                                'lever_rate': int,
                                'margin_account': str,
                                'margin_asset': 'USDT',
                                'margin_mode': 'isolated',
                                'position_margin': Or(float, None),
                                'profit': Or(float, None),
                                'profit_rate': Or(float, None),
                                'profit_unreal': Or(float, None),
                                'symbol': symbol,
                                'volume': Or(float, None),
                                'trade_partition': 'USDT'
                            }
                        ], None),
                        'profit_real': Or(float, None),
                        'profit_unreal': Or(float, None),
                        'risk_rate': Or(float, None),
                        'symbol': symbol,
                        'withdraw_available': Or(float, None)
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
        print(ATP.cancel_all_order())
        print(ATP.close_all_position())


if __name__ == '__main__':
    pytest.main()
