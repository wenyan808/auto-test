#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20211009
# @Author : chenwei
    用例标题
        WS订阅批量Overview(所有合约，即不传contract_code)
    前置条件
        
    步骤/文本
        WS订阅批量Overview(所有合约，即不传contract_code)，可参考文档：https://docs.huobigroup.com/docs/dm/v1/cn/#websocket-3
    预期结果
        open、close、low、high价格正确；amount、vol、count值正确,不存在Null,[]
    优先级
        0
    用例别名
        TestContractNoti_006
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
from common.ContractServiceWS import t as websocketsevice
from tool.atp import ATP

@allure.epic('反向交割')  # 这里填业务线
@allure.feature('WS订阅')  # 这里填功能
@allure.story('行情')  # 这里填子功能，没有的话就把本行注释掉
@allure.tag('Script owner : chenwei', 'Case owner : 吉龙')
class TestContractNoti_006:

    @allure.step('前置条件')
    def setup(self):
        print('''  ''')
        ATP.close_all_position()
        print(''' 使当前交易对有交易盘口  ''')
        print(ATP.make_market_depth())
        print(''' 使当前用户有持仓  ''')

    @allure.title('WS订阅批量Overview(所有合约，即不传contract_code)')
    @allure.step('测试执行')
    def test_execute(self, symbol, symbol_period):
        with allure.step('WS订阅批量Overview(所有合约，即不传contract_code)，可参考文档：https://docs.huobigroup.com/docs/dm/v1/cn/#websocket-3'):
            pass #暂无overview的websocket 说明

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')
        ATP.cancel_all_order()


if __name__ == '__main__':
    pytest.main()
