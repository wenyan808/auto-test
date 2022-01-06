#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20211012
# @Author : chenwei
    用例标题
        WS订阅K线(req) from>to
    前置条件
        
    步骤/文本
        详见官方文档
    预期结果
        
    优先级
        2
    用例别名
        TestContractNoti_ws_kline_084
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
class TestContractNoti_ws_kline_084:

    from_time = None
    to_time = None
    current_price = None

    @allure.step('前置条件')
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, symbol):
        ATP.cancel_all_types_order()
        self.from_time = int(time.time())-7200
        print(''' 构造成交数据 ''')
        ATP.make_market_depth()
        time.sleep(0.5)
        ATP.clean_market()
        time.sleep(1)
        self.current_price = ATP.get_current_price()
        self.to_time = int(time.time())

    @allure.title('WS订阅K线(req) from>to')
    @allure.step('测试执行')
    def test_execute(self, symbol, symbol_period):
        with allure.step('详见官方文档'):
            period = "1mon"
            result = contract_service_ws.contract_req_kline(contract_code=symbol_period, period=period,
                                                            From=self.to_time, to=self.from_time)
            pprint(result)
            tradedetail = result['data']
            if len(tradedetail) != 0:
                assert False

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')
        ATP.cancel_all_order()


if __name__ == '__main__':
    pytest.main()
