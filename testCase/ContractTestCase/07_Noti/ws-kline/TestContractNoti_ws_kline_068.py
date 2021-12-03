#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20211012
# @Author : chenwei
    用例标题
        WS订阅K线(sub) 15min
    前置条件
        
    步骤/文本
        详见官方文档
    预期结果
        id、open、close、low、high价格正确；amount、vol、count值正确,不存在Null,[]
    优先级
        0
    用例别名
        TestContractNoti_ws_kline_068
"""

from common.ContractServiceAPI import t as contract_api
from common.ContractServiceOrder import t as contract_order
from common.LinearServiceAPI import t as linear_api
from common.LinearServiceOrder import t as linear_order
from common.SwapServiceAPI import t as swap_api
from common.SwapServiceOrder import t as swap_order

from pprint import pprint
import pytest
import allure
import random
import time
from common.ContractServiceWS import t as contract_service_ws
from tool.atp import ATP


@allure.epic('反向交割')  # 这里填业务线
@allure.feature('行情')  # 这里填功能
@allure.story('ws k线')  # 这里填子功能，没有的话就把本行注释掉
@pytest.mark.stable
@allure.tag('Script owner : chenwei', 'Case owner : 吉龙')
class TestContractNoti_ws_kline_068:

    @allure.step('前置条件')
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, symbol):
        print(" 清盘 -》 挂单 ")
        ATP.cancel_all_types_order()
        time.sleep(0.5)
        ATP.make_market_depth()
        self.current_price = ATP.get_current_price()
        sell_price = round(self.current_price * 1.02, 2)
        buy_price = round(self.current_price * 0.98, 2)
        ATP.common_user_make_order(price=sell_price, direction='sell')
        ATP.common_user_make_order(price=buy_price, direction='buy')
        time.sleep(1)

    @allure.title('WS订阅K线(sub) 15min')
    @allure.step('测试执行')
    def test_execute(self, symbol, symbol_period):
        with allure.step('详见官方文档'):
            period = "15min"
            result = contract_service_ws.contract_sub_kline(
                contract_code=symbol_period, period=period)
            pprint(result)
            if 'tick' in result:
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


if __name__ == '__main__':
    pytest.main()
