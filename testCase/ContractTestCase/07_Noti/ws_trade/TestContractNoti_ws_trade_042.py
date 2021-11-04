#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20211019
# @Author : 
    用例标题
        WS订阅成交(req)  最优10档成交
    前置条件
        
    步骤/文本
        详见官方文档
    预期结果
        
    优先级
        1
    用例别名
        TestContractNoti_ws_trade_042
"""

from common.ContractServiceAPI import t as contract_api
from common.ContractServiceOrder import t as contract_order
from common.LinearServiceAPI import t as linear_api
from common.LinearServiceOrder import t as linear_order
from common.SwapServiceAPI import t as swap_api
from common.SwapServiceOrder import t as swap_order

from pprint import pprint
import pytest, allure, random, time
from tool.atp import ATP
from common.ContractServiceWS import t as contract_service_ws

@allure.epic('反向交割')  # 这里填业务线
@allure.feature('行情')  # 这里填功能
@allure.story('成交')  # 这里填子功能，没有的话就把本行注释掉
@pytest.mark.stable
@allure.tag('Script owner : chenwei', 'Case owner : 吉龙')
class TestContractNoti_ws_trade_042:

    @allure.step('前置条件')
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, symbol):
        ATP.cancel_all_types_order()
        time.sleep(1)
        self.current_price = ATP.get_current_price()
        print(''' make market depth ''')
        ATP.make_market_depth()
        sell_price = ATP.get_adjust_price(1.02)
        buy_price = ATP.get_adjust_price(0.98)
        ATP.common_user_make_order(price=sell_price, order_price_type='optimal_10',  direction='sell')
        ATP.common_user_make_order(price=buy_price, order_price_type='optimal_10', direction='buy')
        time.sleep(2)
        self.current_price = ATP.get_current_price()

    @allure.title('WS订阅成交(req)  最优10档成交')
    @allure.step('测试执行')
    def test_execute(self, symbol, symbol_period):
        with allure.step('详见官方文档'):
            result = contract_service_ws.contract_req_tradedetail(symbol_period)
            pprint(result)
            tradedetail = result['data'][0]
            if tradedetail['amount'] == None:
                assert False
            if tradedetail['direction'] == None:
                assert False
            if float(tradedetail['price']) != float(self.current_price):
                assert False
            if tradedetail['quantity'] == None:
                assert False
            if tradedetail['id'] == None:
                assert False

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')
        ATP.cancel_all_order()


if __name__ == '__main__':
    pytest.main()
