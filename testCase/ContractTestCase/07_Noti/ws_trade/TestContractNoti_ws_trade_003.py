#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20211019
# @Author : 
    用例标题
        WS订阅成交(sub)  不传合约代码
    前置条件
        
    步骤/文本
        详见官方文档
    预期结果
        
    优先级
        1
    用例别名
        TestContractNoti_ws_trade_003
"""
from pprint import pprint
import pytest
import allure
import random
import time
from tool.atp import ATP
from common.ContractServiceWS import t as contract_service_ws


@allure.epic('反向交割')  # 这里填业务线
@allure.feature('行情')  # 这里填功能
@allure.story('成交')  # 这里填子功能，没有的话就把本行注释掉
@pytest.mark.stable
@allure.tag('Script owner : chenwei', 'Case owner : 吉龙')
class TestContractNoti_ws_trade_003:

    from_time = None
    to_time = None
    current_price = None

    @allure.step('前置条件')
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, symbol):
        ATP.cancel_all_types_order()
        self.from_time = int(time.time())
        print(''' 构造成交数据 ''')
        ATP.make_market_depth()
        time.sleep(0.5)
        ATP.clean_market()
        time.sleep(1)
        self.current_price = ATP.get_current_price()
        self.to_time = int(time.time())
        ATP.common_user_make_order(price=self.current_price, direction='sell')
        time.sleep(1)
        ATP.common_user_make_order(price=self.current_price, direction='buy')
        time.sleep(1)

    @allure.title('WS订阅成交(sub)  不传合约代码')
    @allure.step('测试执行')
    def test_execute(self, symbol, symbol_period):
        with allure.step('详见官方文档'):
            result = contract_service_ws.contract_sub_tradedetail()
            pprint(result)
            errmsg = result['err-msg']
            if errmsg != "invalid topic market.NONE.trade.detail":
                assert False

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')
        ATP.cancel_all_order()


if __name__ == '__main__':
    pytest.main()
