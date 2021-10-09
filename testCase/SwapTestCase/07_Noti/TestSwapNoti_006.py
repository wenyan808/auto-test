#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20211009
# @Author : 
    用例标题
        WS订阅批量Overview(所有合约，即不传contract_code)
    前置条件
        
    步骤/文本
        WS订阅批量Overview(所有合约，即不传contract_code)，可参考文档：https://docs.huobigroup.com/docs/coin_margined_swap/v1/cn/#websocket-3
    预期结果
        open、close、low、high价格正确；amount、vol、count值正确,不存在Null,[]
    优先级
        0
    用例别名
        TestSwapNoti_006
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
from common.SwapServiceWS import t as websocketsevice

@allure.epic('业务线')  # 这里填业务线
@allure.feature('功能')  # 这里填功能
@allure.story('子功能')  # 这里填子功能，没有的话就把本行注释掉
class TestSwapNoti_006:

    @allure.step('前置条件')
    def setup(self):
        ATP.close_all_position()
        print(''' 使当前交易对有交易盘口  ''')
        print(ATP.make_market_depth())
        print(''' 使当前用户有持仓  ''')

    @allure.title('WS订阅批量Overview(所有合约，即不传contract_code)')
    @allure.step('测试执行')
    def test_execute(self, contract_code):
        with allure.step('WS订阅批量Overview(所有合约，即不传contract_code)，可参考文档：https://docs.huobigroup.com/docs/coin_margined_swap/v1/cn/#websocket-3'):
            r = websocketsevice.swap_sub_detail(contract_code=contract_code)
            pprint(r)
            tradedetail = r['tick']
            if tradedetail['amount'] == None:
                assert False
            if tradedetail['close'] == None:
                assert False
            if tradedetail['count'] == None:
                assert False
            if tradedetail['high'] == None:
                assert False
            if tradedetail['low'] == None:
                assert False
            if tradedetail['open'] == None:
                assert False
            if tradedetail['vol'] == None:
                assert False

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')
        ATP.cancel_all_trigger_order()
        ATP.cancel_all_order()
        ATP.close_all_position()


if __name__ == '__main__':
    pytest.main()
