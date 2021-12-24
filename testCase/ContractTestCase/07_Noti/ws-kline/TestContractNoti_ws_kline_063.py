#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20211012
# @Author : chenwei
    用例标题
        WS订阅K线(sub) 合约代码大写
    前置条件
        
    步骤/文本
        详见官方文档
    预期结果
        
    优先级
        3
    用例别名
        TestContractNoti_ws_kline_063
"""

import time
from pprint import pprint

import allure
import pytest
from common.ContractServiceWS import t as contract_service_ws
from tool.atp import ATP


@allure.epic('反向交割')  # 这里填业务线
@allure.feature('行情')  # 这里填功能
@allure.story('ws k线')  # 这里填子功能，没有的话就把本行注释掉
@pytest.mark.stable
@allure.tag('Script owner : chenwei', 'Case owner : 吉龙')
class TestContractNoti_ws_kline_063:

    from_time = None
    to_time = None
    current_price = None

    @allure.step('前置条件')
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, symbol):
        ATP.cancel_all_types_order()
        self.from_time = int(time.time())
        print(''' 制造成交数据 ''')
        ATP.make_market_depth()

        self.current_price = ATP.get_current_price()
        self.to_time = int(time.time())

    @allure.title('WS订阅K线(sub) 合约代码大写')
    @allure.step('测试执行')
    def test_execute(self, symbol, symbol_period):
        with allure.step('详见官方文档'):
            period = "1min"
            result = contract_service_ws.contract_sub_kline(
                contract_code=symbol_period.upper(), period=period)
            pprint(result)
            tradedetail = result['tick']
            if tradedetail['amount'] == None:
                assert False
            if tradedetail['close'] == None:
                assert False
            if tradedetail['count'] == None:
                assert False
            if tradedetail['high'] == None:
                assert False
            if tradedetail['id'] == None:
                assert False
            if tradedetail['low'] == None:
                assert False
            if tradedetail['mrid'] == None:
                assert False
            if tradedetail['open'] == None:
                assert False
            if tradedetail['vol'] == None:
                assert False

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')
        ATP.cancel_all_order()
        ATP.clean_market()


if __name__ == '__main__':
    pytest.main()
