#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20211009
# @Author : 
    用例标题
        WS订阅BBO(单个合约，即传参合约code)
    前置条件
        
    步骤/文本
        WS订阅BBO(单个合约，即传参合约code)，可参考文档：https://docs.huobigroup.com/docs/usdt_swap/v1/cn/#websocket-3
    预期结果
        asks,bids 数据正确,不存在Null,[]
    优先级
        0
    用例别名
        TestLinearNoti_004
"""

from common.ContractServiceAPI import t as contract_api
from common.ContractServiceOrder import t as contract_order
from common.LinearServiceAPI import t as linear_api
from common.LinearServiceOrder import t as linear_order
from common.SwapServiceAPI import t as swap_api
from common.SwapServiceOrder import t as swap_order

from pprint import pprint
import pytest, allure, random, time
from common.LinearServiceWS import t as linear_service_ws


@allure.epic('正向永续')  # 这里填业务线
@allure.feature('WS订阅')  # 这里填功能
@allure.story('订阅BBO')  # 这里填子功能，没有的话就把本行注释掉
@pytest.mark.stable
class TestLinearNoti_004:

    @allure.step('前置条件')
    def setup(self):
        lever_rate = 5
        contractCode = 'BTC-USDT'
        order_price_type = 'limit'
        offset = 'open'
        buyPrice = '45000'
        sellPrice = '50000'
        buy = 'buy'
        sell = 'sell'
        print('进行挂单，更新买卖单数据')
        linear_api.linear_order(contract_code=contractCode, price=buyPrice, order_price_type=order_price_type,
                                lever_rate=lever_rate,
                                direction=buy, offset=offset,
                                volume=10)
        linear_api.linear_order(contract_code=contractCode, price=sellPrice, order_price_type=order_price_type,
                                lever_rate=lever_rate,
                                direction=sell, offset=offset,
                                volume=10)
        # 等待深度更新
        time.sleep(3)

    @allure.title('WS订阅BBO(单个合约，即传参合约code)')
    @allure.step('测试执行')
    def test_execute(self):
        with allure.step('WS订阅BBO(单个合约，即传参合约code)，可参考文档：https://docs.huobigroup.com/docs/usdt_swap/v1/cn/#websocket-3'):
            contractCode = 'BTC-USDT'
            result = linear_service_ws.linear_sub_bbo(contract_code=contractCode)
            resultStr = '\nDepth返回结果 = ' + str(result)
            print('\033[1;32;49m%s\033[0m' % resultStr)
            if not result['tick']['bid']:
                assert False
            if not result['tick']['ask']:
                assert False
            pass

    @allure.step('恢复环境')
    def teardown(self):
        print('')


if __name__ == '__main__':
    pytest.main()
