#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20211028
# @Author : 
    用例标题
        撮合当周 正常结算发起的订单                
    前置条件
        
    步骤/文本
        详见官方文档
    预期结果
        正确撮合
    优先级
        1
    用例别名
        TestContractEx_081
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
from tool.atp import ATP
from common.mysqlComm import orderSeq as DB_orderSeq


@allure.epic('反向交割')  # 这里填业务线
@allure.feature('撮合')  # 这里填功能
@allure.story('委托单')  # 这里填子功能，没有的话就把本行注释掉
@pytest.mark.stable
@allure.tag('Script owner : chenwei', 'Case owner : 邱大伟')
class TestContractEx_081:

    @allure.step('前置条件')
    def setup(self):
        print(''' 制造成交数据 ''')
        ATP.make_market_depth(depth_count=5)
        sell_price = ATP.get_adjust_price(1.02)
        buy_price = ATP.get_adjust_price(0.98)
        ATP.common_user_make_order(price=sell_price, direction='sell')
        ATP.common_user_make_order(price=buy_price, direction='buy')
        time.sleep(1)

    @allure.title('撮合当周 正常结算发起的订单                ')
    @allure.step('测试执行')
    def test_execute(self, symbol, symbol_period):
        with allure.step('详见官方文档'):
            pass  # 不方便构造结算场景

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')
        ATP.cancel_all_types_order()


if __name__ == '__main__':
    pytest.main()
