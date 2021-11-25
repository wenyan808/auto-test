#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20211122
# @Author : 
    用例标题
        获取用户的合约订单信息（全仓）
    前置条件
        
    步骤/文本
        调用接口：/linear-swap-api/v1/swap_cross_order_info
    预期结果
        A)接口返回的json格式、字段名、字段值正确
    优先级
        0
    用例别名
        TestLinearApiSchema_088
"""
import random
import time
from pprint import pprint

import allure
import pytest
from schema import Schema, Or
from tool import atp
from common.LinearServiceAPI import t as linear_api


@allure.epic('正向永续')  # 这里填业务线
@allure.feature('api')  # 这里填功能
@allure.story('schema校验')  # 这里填子功能，没有的话就把本行注释掉
@allure.tag('Script owner : 张广南', 'Case owner : 张让翰')
@pytest.mark.stable
class TestLinearApiSchema_088:

    @allure.step('前置条件')
    def setup(self):
        self.price = atp.ATP.get_adjust_price(rate=0.98)

    @allure.title('获取用户的合约订单信息（全仓）')
    @allure.step('测试执行')
    def test_execute(self, contract_code, symbol):
        with allure.step('调用接口：/linear-swap-api/v1/swap_cross_order_info'):
            a = linear_api.linear_cross_order(contract_code=contract_code,
                                              client_order_id='',
                                              price=self.price,
                                              volume='1',
                                              direction='buy',
                                              offset='open',
                                              lever_rate=5,
                                              order_price_type='limit')

            time.sleep(1)
            order_id = a['data']['order_id']
            r = linear_api.linear_cross_order_info(contract_code=contract_code,
                                             order_id=order_id)
            pprint(r)
            schema = {
                'data': [
                    {
                        'canceled_at': int,
                        'client_order_id': Or(None, int),
                        'contract_code': contract_code,
                        'created_at': int,
                        'direction': str,
                        'fee': Or(int, float),
                        'fee_asset': 'USDT',
                        'is_tpsl': Or(0, 1),
                        'lever_rate': int,
                        'liquidation_type': str,
                        'margin_account': str,
                        'margin_asset': 'USDT',
                        'margin_frozen': Or(float, None),
                        'margin_mode': 'cross',
                        'offset': str,
                        'order_id': int,
                        'order_id_str': str,
                        'order_price_type': str,
                        'order_source': str,
                        'order_type': int,
                        'price': Or(int, float),
                        'profit': Or(int, float),
                        'real_profit': Or(int, float),
                        'status': int,
                        'symbol': symbol,
                        'trade_avg_price': Or(int, float, None),
                        'trade_turnover': Or(float, int),
                        'trade_volume': int,
                        'update_time': Or(int, None),
                        'volume': int,
                        'business_type': 'swap',
                        'contract_type': 'swap',
                        'pair': 'ETH-USDT'
                    }
                ],
                'status': 'ok',
                'ts': int
            }

            Schema(schema).validate(r)

    @allure.step('恢复环境')
    def teardown(self):
        time.sleep(2)
        print(atp.ATP.cancel_all_order())
        print('\n恢复环境操作')


if __name__ == '__main__':
    pytest.main()
