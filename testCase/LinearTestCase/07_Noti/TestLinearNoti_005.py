#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20211009
# @Author : 
    用例标题
        WS订阅聚合行情(单个合约，即传参contract_code)
    前置条件
        
    步骤/文本
        WS订阅聚合行情(单个合约，即传参contract_code)，可参考文档：https://docs.huobigroup.com/docs/usdt_swap/v1/cn/#websocket-3
    预期结果
        open、close、low、high价格正确；amount、vol、count值正确asks、bid值正确,不存在Null,[]
    优先级
        0
    用例别名
        TestLinearNoti_005
"""

from common.LinearServiceAPI import t as linear_api
from common.LinearServiceWS import t as linear_service_ws
import pytest, allure, random, time
from tool.atp import ATP
from common.LinearServiceWS import t as websocketsevice

@allure.epic('正向永续')  # 这里填业务线
@allure.feature('WS订阅')  # 这里填功能
@allure.story('订阅聚合行情')  # 这里填子功能，没有的话就把本行注释掉
@pytest.mark.stable
class TestLinearNoti_005:

    @allure.step('前置条件')
    def setup(self):
        ATP.close_all_position()
        print(''' 使当前交易对有交易盘口  ''')
        print(ATP.make_market_depth())

    @allure.title('WS订阅聚合行情(单个合约，即传参contract_code)')
    @allure.step('测试执行')
    def test_execute(self, contract_code):
        with allure.step('WS订阅聚合行情(单个合约，即传参contract_code)，可参考文档：https://docs.huobigroup.com/docs/usdt_swap/v1/cn/#websocket-3'):

            result = websocketsevice.linear_sub_detail(contract_code=contract_code)
            resultStr = '\n聚合行情（Market detail ）返回结果 = ' + str(result)
            print('\033[1;32;49m%s\033[0m' % resultStr)
            if not result['tick']['bid']:
                assert False
            if not result['tick']['ask']:
                assert False
            pass

    @allure.step('恢复环境')
    def teardown(self):
        ATP.cancel_all_types_order()
        print('\n恢复环境操作')


if __name__ == '__main__':
    pytest.main()
