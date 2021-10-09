#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20211009
# @Author : chenwei
    用例标题
        WS订阅最新成交记录(单个合约，即传参contract_code)
    前置条件
        
    步骤/文本
        WS订阅最新成交记录(单个合约，即传参contract_code)，可参考文档：https://docs.huobigroup.com/docs/usdt_swap/v1/cn/#websocket-3
    预期结果
        amount\quantity\turnover\direction\price显示正确,不存在Null,[]
    优先级
        0
    用例别名
        TestLinearNoti_007
"""

from common.ContractServiceAPI import t as contract_api
from common.ContractServiceOrder import t as contract_order
from common.LinearServiceAPI import t as linear_api
from common.LinearServiceOrder import t as linear_order
from common.SwapServiceAPI import t as swap_api
from common.SwapServiceOrder import t as swap_order
from common.LinearServiceWS import WebsocketSevice as websocketsevice
from pprint import pprint
import pytest, allure, random, time


@allure.epic('业务线')  # 这里填业务线
@allure.feature('功能')  # 这里填功能
@allure.story('子功能')  # 这里填子功能，没有的话就把本行注释掉
class TestLinearNoti_007:

    @allure.step('前置条件')
    def setup(self):
        print('''  ''')

    @allure.title('WS订阅最新成交记录(单个合约，即传参contract_code)')
    @allure.step('测试执行')
    def test_execute(self, contract_code, symbol_period):
        with allure.step('WS订阅最新成交记录(单个合约，即传参contract_code)，可参考文档：https://docs.huobigroup.com/docs/usdt_swap/v1/cn/#websocket-3'):
            r = websocketsevice.linear_req_trade_detail(contract_code)
            pprint(r)

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')


if __name__ == '__main__':
    pytest.main()
