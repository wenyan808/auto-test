#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20211013
# @Author : 
    用例标题
        restful请求K线 1mon 只传from,不传to
    前置条件
        
    步骤/文本
        详见官方文档
    预期结果
        
    优先级
        2
    用例别名
        TestLinearNoti_restful_kline_076
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

@allure.epic('业务线')  # 这里填业务线
@allure.feature('功能')  # 这里填功能
@allure.story('子功能')  # 这里填子功能，没有的话就把本行注释掉
@pytest.mark.stable
class TestLinearNoti_restful_kline_076:

    from_time = None
    to_time = None
    current_price = None

    @allure.step('前置条件')
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, contract_code):
        ATP.cancel_all_types_order()
        self.from_time = int(time.time())
        print(''' 制造成交数据 ''')
        ATP.make_market_depth()
        time.sleep(0.5)
        ATP.clean_market()
        time.sleep(1)
        self.current_price = ATP.get_current_price()
        self.to_time = int(time.time())

    @allure.title('restful请求K线 1mon 只传from,不传to')
    @allure.step('测试执行')
    def test_execute(self, contract_code):
        with allure.step('详见官方文档'):
            r = linear_api.linear_kline(contract_code=contract_code, period="1mon", size=2, FROM=self.from_time)
            pprint(r)
            klinedata = r['data'][0]
            if klinedata['amount'] == None:
                assert False
            if klinedata['close'] == None:
                assert False
            if klinedata['count'] == None:
                assert False
            if klinedata['high'] == None:
                assert False
            if klinedata['id'] == None:
                assert False
            if klinedata['low'] == None:
                assert False
            if klinedata['open'] == None:
                assert False
            if klinedata['trade_turnover'] == None:
                assert False
            if klinedata['vol'] == None:
                assert False

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')
        ATP.clean_market()


if __name__ == '__main__':
    pytest.main()
