#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20211009
# @Author : 
    用例标题
        WS订阅深度(20档不合并，即传参step6)
    前置条件
        
    步骤/文本
        WS订阅深度(20档不合并，即传参step6)，可参考文档：https://docs.huobigroup.com/docs/coin_margined_swap/v1/cn/#websocket-3
    预期结果
        asks,bids 数据正确,不存在Null,[]
    优先级
        0
    用例别名
        TestSwapNoti_003
"""

from common.SwapServiceWS import t as swap_service_ws
from common.SwapServiceAPI import t as swap_api
from common.SwapServiceOrder import t as swap_order
from tool import atp
from pprint import pprint
import pytest, allure, random, time

@allure.epic('反向永续')  # 这里填业务线
@allure.feature('WS订阅')  # 这里填功能
@allure.story('深度|20档不合并')  # 这里填子功能，没有的话就把本行注释掉
@pytest.mark.stable
class TestSwapNoti_003:

    @allure.step('前置条件')
    def setup(self):
        contract_code = 'BTC-USD'
        print("\n清卖盘》》》》", atp.ATP.clean_market(contract_code=contract_code, direction='sell'))
        print("\n清买盘》》》》", atp.ATP.clean_market(contract_code=contract_code, direction='buy'))
        lever_rate = 5
        order_price_type = 'limit'
        offset = 'open'
        buy = 'buy'
        sell = 'sell'

        print('进行2笔交易，更新Kline数据')
        swap_api.swap_order(contract_code=contract_code, price='50000', volume=1, direction=buy, offset=offset,
                            lever_rate=lever_rate, order_price_type=order_price_type)

        swap_api.swap_order(contract_code=contract_code, price='50001', volume=1, direction=sell, offset=offset,
                            lever_rate=lever_rate, order_price_type=order_price_type)

    @allure.title('WS订阅深度(20档不合并，即传参step6)')
    @allure.step('测试执行')
    def test_execute(self):
        with allure.step('WS订阅深度(20档不合并，即传参step6)，可参考文档：https://docs.huobigroup.com/docs/coin_margined_swap/v1/cn/#websocket-3'):
            contractCode = 'BTC-USD'
            depthType = 'step6'
            result = swap_service_ws.swap_sub_depth(contract_code=contractCode, type=depthType)
            resultStr = '\nDepth返回结果 = ' + str(result)
            print('\033[1;32;49m%s\033[0m' % resultStr)
            if not result['tick']['bids']:
                assert False
            if not result['tick']['asks']:
                assert False
            pass

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')


if __name__ == '__main__':
    pytest.main()
