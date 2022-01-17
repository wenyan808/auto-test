#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20211122
# @Author : 
    用例标题
        查询开仓单关联的止盈止损订单详情（逐仓）
    前置条件
        
    步骤/文本
        调用接口：/linear-swap-api/v1/swap_relation_tpsl_order
    预期结果
        A)接口返回的json格式、字段名、字段值正确
    优先级
        0
    用例别名
        TestLinearApiSchema_067
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
class TestLinearApiSchema_067:

    @allure.step('前置条件')
    def setup(self):
        pass

    @allure.title('查询开仓单关联的止盈止损订单详情（逐仓）')
    @allure.step('测试执行')
    def test_execute(self, contract_code, symbol):
        with allure.step('调用接口：/linear-swap-api/v1/swap_relation_tpsl_order'):
            lastprice = ATP.get_adjust_price(rate=1)
            tp_price = ATP.get_adjust_price(rate=1.05)
            sl_price = ATP.get_adjust_price(rate=0.95)

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
                                                order_price_type="limit",
                                                tp_trigger_price=tp_price,
                                                tp_order_price=tp_price,
                                                tp_order_price_type='limit',
                                                sl_order_price=sl_price,
                                                sl_order_price_type='limit',
                                                sl_trigger_price=sl_price)
            pprint(buy_order)

            time.sleep(2)
            order_id = buy_order['data']['order_id']
            trade_partition = linear_api.get_trade_partition(contract_code)
            r = linear_api.linear_relation_tpsl_order(contract_code=contract_code,
                                                      order_id=order_id)
            pprint(r)
            schema = {'data': {'canceled_at': int,
                               'client_order_id': Or(int, str, None),
                               'contract_code': contract_code,
                               'created_at': int,
                               'direction': str,
                               'fee': Or(float, int),
                               'fee_asset': trade_partition,
                               'lever_rate': int,
                               'margin_account': contract_code,
                               'margin_frozen': float,
                               'margin_mode': 'isolated',
                               'offset': str,
                               'order_id': int,
                               'order_id_str': str,
                               'order_price_type': str,
                               'order_source': str,
                               'order_type': int,
                               'price': Or(int, float),
                               'profit': Or(int, float),
                               'status': int,
                               'symbol': str,
                               'trade_partition': trade_partition,
                               'tpsl_order_info': [{'canceled_at': int,
                                                    'created_at': int,
                                                    'direction': str,
                                                    'fail_code': Or(None, str),
                                                    'fail_reason': Or(None, str),
                                                    'order_id': int,
                                                    'order_id_str': str,
                                                    'order_price': float,
                                                    'order_price_type': str,
                                                    'relation_order_id': str,
                                                    'relation_tpsl_order_id': str,
                                                    'status': int,
                                                    'tpsl_order_type': str,
                                                    'trigger_price': float,
                                                    'trigger_type': str,
                                                    'triggered_price': Or(int, float, None),
                                                    'volume': float}, ],
                               'trade_avg_price': Or(float, None),
                               'trade_turnover': Or(float, int),
                               'trade_volume': int,
                               'volume': int},
                      'status': 'ok',
                      'ts': int}

            Schema(schema).validate(r)

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')
        print(ATP.cancel_all_tpsl_order())
        print(ATP.cancel_all_order())
        #print(ATP.close_all_position())


if __name__ == '__main__':
    pytest.main()
