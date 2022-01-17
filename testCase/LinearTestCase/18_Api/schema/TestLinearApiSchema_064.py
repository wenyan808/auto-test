#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20211122
# @Author : 
    用例标题
        止盈止损全部撤单（逐仓）
    前置条件
        
    步骤/文本
        调用接口：/linear-swap-api/v1/swap_tpsl_cancelall
    预期结果
        A)接口返回的json格式、字段名、字段值正确
    优先级
        0
    用例别名
        TestLinearApiSchema_064
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
class TestLinearApiSchema_064:

    @allure.step('前置条件')
    def setup(self):
        pass

    @allure.title('止盈止损全部撤单（逐仓）')
    @allure.step('测试执行')
    def test_execute(self, contract_code, symbol):
        with allure.step('调用接口：/linear-swap-api/v1/swap_tpsl_cancelall'):
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
                                                order_price_type="limit")
            pprint(buy_order)

            time.sleep(2)
            a = linear_api.linear_tpsl_order(contract_code=contract_code,
                                             direction='sell',
                                             volume='1',
                                             tp_trigger_price=tp_price,
                                             tp_order_price=tp_price,
                                             tp_order_price_type='limit',
                                             sl_order_price=sl_price,
                                             sl_order_price_type='limit',
                                             sl_trigger_price=sl_price)
            time.sleep(1)
            r = linear_api.linear_tpsl_cancelall(contract_code=contract_code)
            pprint(r)
            schema = {'data': {'errors': list,
                               'successes': str},
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
