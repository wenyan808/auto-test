#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20211014
# @Author : 
    用例标题
        查询基差15min K线
    前置条件
        
    步骤/文本
        详见官方文档
    预期结果
        180条数据,K线不间断,最后一根是当前时间
    优先级
        0
    用例别名
        TestLinearExIndex_basis_003
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
from common.LinearServiceWS import t as websocketsevice

@allure.epic('业务线')  # 这里填业务线
@allure.feature('功能')  # 这里填功能
@allure.story('子功能')  # 这里填子功能，没有的话就把本行注释掉
class TestLinearExIndex_basis_003:

    @allure.step('前置条件')
    def setup(self):
        print(''' cancel all types orders ''')
        ATP.cancel_all_types_order()
        time.sleep(1)
        self.current_price = ATP.get_current_price()
        print(''' make market depth ''')
        ATP.make_market_depth()
        sell_price = ATP.get_adjust_price(1.02)
        buy_price = ATP.get_adjust_price(0.98)
        ATP.common_user_make_order(price=sell_price, direction='sell')
        ATP.common_user_make_order(price=buy_price, direction='buy')
        time.sleep(2)

    @allure.title('查询基差15min K线')
    @allure.step('测试执行')
    def test_execute(self, contract_code):
        with allure.step('详见官方文档'):
            period = "15min"
            r = websocketsevice.linear_sub_index(contract_code, period)
            pprint(r)
            tick = r['tick']
            if tick['amount'] == None:
                assert False
            if tick['close'] == None:
                assert False
            if tick['count'] == None:
                assert False
            if tick['high'] == None:
                assert False
            if tick['id'] == None:
                assert False
            if tick['low'] == None:
                assert False
            if tick['open'] == None:
                assert False
            if tick['vol'] == None:
                assert False

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')
        ATP.clean_market()


if __name__ == '__main__':
    pytest.main()
