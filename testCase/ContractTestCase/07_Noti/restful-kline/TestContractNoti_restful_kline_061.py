#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20211015
# @Author : 
    用例标题
        restful请求K线 1day to传参错误 非时间戳
    前置条件
        
    步骤/文本
        详见官方文档
    预期结果
        
    优先级
        3
    用例别名
        TestContractNoti_restful_kline_061
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

@allure.epic('反向交割')  # 这里填业务线
@allure.feature('行情')  # 这里填功能
@allure.story('restful K线')  # 这里填子功能，没有的话就把本行注释掉
@pytest.mark.stable
class TestContractNoti_restful_kline_061:

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
        time.sleep(0.5)
        ATP.clean_market()
        time.sleep(1)
        self.current_price = ATP.get_current_price()
        self.to_time = int(time.time())

    @allure.title('restful请求K线 1day to传参错误 非时间戳')
    @allure.step('测试执行')
    def test_execute(self, symbol, symbol_period):
        with allure.step('详见官方文档'):
            period = "1day"
            result = contract_api.contract_kline(symbol=symbol_period, period=period, to="abce")
            pprint(result)
            errmsg = result['err-msg']
            if errmsg != "from cannot be empty":
                assert False

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')
        ATP.clean_market()


if __name__ == '__main__':
    pytest.main()
