#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20211009
# @Author : chenwei
    用例标题
        WS订阅批量成交记录(单个合约，即传参contract_code)
    前置条件
        
    步骤/文本
        WS订阅批量成交记录(单个合约，即传参contract_code)，可参考文档：https://docs.huobigroup.com/docs/usdt_swap/v1/cn/#websocket-3
    预期结果
        amount\quantity\turnover\direction\price显示正确,不存在Null,[]
    优先级
        0
    用例别名
        TestLinearNoti_008
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
class TestLinearNoti_008:

    @allure.step('前置条件')
    def setup(self):
        ATP.close_all_position()
        print(''' 使当前交易对有交易盘口  ''')
        print(ATP.make_market_depth())

    @allure.title('WS订阅批量成交记录(单个合约，即传参contract_code)')
    @allure.step('测试执行')
    def test_execute(self, contract_code):
        with allure.step('WS订阅批量成交记录(单个合约，即传参contract_code)，可参考文档：https://docs.huobigroup.com/docs/usdt_swap/v1/cn/#websocket-3'):
            r = websocketsevice.linear_req_trade_detail(contract_code=contract_code)
            pprint(r)
            tradedetail = r['data'][0]
            if tradedetail['amount'] == None:
                assert False
            if tradedetail['direction'] == None:
                assert False
            if tradedetail['price'] == None:
                assert False
            if tradedetail['quantity'] == None:
                assert False
            if tradedetail['trade_turnover'] == None:
                assert False

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')
        ATP.cancel_all_trigger_order()
        ATP.cancel_all_order()
        ATP.close_all_position()


if __name__ == '__main__':
    pytest.main()
