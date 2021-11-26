#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20211122
# @Author : 
    用例标题
        获取计划委托当前委托（全仓）
    前置条件
        
    步骤/文本
        调用接口：/linear-swap-api/v1/swap_cross_trigger_openorders
    预期结果
        A)接口返回的json格式、字段名、字段值正确
    优先级
        0
    用例别名
        TestLinearApiSchema_099
"""
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
class TestLinearApiSchema_099:

    @allure.step('前置条件')
    def setup(self):
        self.buyprice = atp.ATP.get_adjust_price(rate=0.98)

    @allure.title('获取计划委托当前委托（全仓）')
    @allure.step('测试执行')
    def test_execute(self, contract_code, symbol):
        with allure.step('调用接口：/linear-swap-api/v1/swap_cross_trigger_openorders'):
            a = linear_api.linear_cross_trigger_order(contract_code=contract_code,
                                                      trigger_type='le',
                                                      trigger_price=self.buyprice,
                                                      order_price=self.buyprice,
                                                      order_price_type='limit',
                                                      volume='1',
                                                      direction='buy',
                                                      offset='open',
                                                      lever_rate=5)
            time.sleep(1)
            r = linear_api.linear_cross_trigger_openorders(contract_code=contract_code,
                                                  page_index='',
                                                  page_size='')
            pprint(r)
            schema = {
                'data': {
                    'current_page': int,
                    'orders': [
                        {
                            'contract_code': contract_code,
                            'created_at': int,
                            'direction': str,
                            'lever_rate': int,
                            'margin_account': str,
                            'margin_mode': 'cross',
                            'offset': str,
                            'order_id': int,
                            'order_id_str': str,
                            'order_price': float,
                            'order_price_type': str,
                            'order_source': str,
                            'order_type': int,
                            'status': int,
                            'symbol': symbol,
                            'trigger_price': float,
                            'trigger_type': str,
                            'volume': float,
                            'contract_type': 'swap',
                            'business_type': 'swap',
                            'pair': str

                        }
                    ],
                    'total_page': int,
                    'total_size': int
                },
                'status': 'ok',
                'ts': int
            }

            Schema(schema).validate(r)

    @allure.step('恢复环境')
    def teardown(self):
        print(atp.ATP.cancel_all_trigger_order())
        print('\n恢复环境操作')


if __name__ == '__main__':
    pytest.main()
