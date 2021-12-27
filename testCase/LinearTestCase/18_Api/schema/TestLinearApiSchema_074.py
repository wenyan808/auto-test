#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20211122
# @Author : 
    用例标题
        获取用户的合约持仓信息（全仓）
    前置条件
        
    步骤/文本
        调用接口：/linear-swap-api/v1/swap_cross_position_info
    预期结果
        A)接口返回的json格式、字段名、字段值正确
    优先级
        0
    用例别名
        TestLinearApiSchema_074
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
class TestLinearApiSchema_074:

    @allure.step('前置条件')
    def setup(self):
        print('''  ''')

    @allure.title('获取用户的合约持仓信息（全仓）')
    @allure.step('测试执行')
    def test_execute(self, contract_code, symbol):
        with allure.step('调用接口：/linear-swap-api/v1/swap_cross_position_info'):
            lastprice = ATP.get_current_price()

            sell_order = linear_api.linear_cross_order(contract_code=contract_code,
                                                       price=lastprice,
                                                       volume='1',
                                                       direction='sell',
                                                       offset='open',
                                                       order_price_type="limit")
            pprint(sell_order)

            buy_order = linear_api.linear_cross_order(contract_code=contract_code,
                                                      price=lastprice,
                                                      volume='1',
                                                      direction='buy',
                                                      offset='open',
                                                      order_price_type="limit")
            pprint(buy_order)

            time.sleep(1)
            r = linear_api.linear_cross_position_info(contract_code=contract_code)
            pprint(r)
            schema = {
                'data': [
                    {
                        'symbol': symbol,
                        'contract_code': contract_code,
                        'volume': float,
                        'available': float,
                        'frozen': Or(float, None),
                        'cost_open': float,
                        'cost_hold': float,
                        'profit_unreal': float,
                        'profit_rate': float,
                        'profit': float,
                        'margin_asset': 'USDT',
                        'position_margin': float,
                        'lever_rate': int,
                        'margin_account': str,
                        'margin_mode': 'cross',
                        'direction': str,
                        'contract_type': 'swap',
                        'business_type': 'swap',
                        'pair': str,
                        'last_price': Or(float, int),
                        'trade_partition': 'USDT'
                    }
                ],
                'status': 'ok',
                'ts': int
            }

            Schema(schema).validate(r)

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')
        print(ATP.cancel_all_order())
        print(ATP.close_all_position())


if __name__ == '__main__':
    pytest.main()
