#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20211009
# @Author : 
    用例标题
        WS订阅BBO(单个合约，即传参合约code)
    前置条件
        
    步骤/文本
        WS订阅BBO(单个合约，即传参合约code)，可参考文档：https://docs.huobigroup.com/docs/coin_margined_swap/v1/cn/#websocket-3
    预期结果
        asks,bids 数据正确,不存在Null,[]
    优先级
        0
    用例别名
        TestSwapNoti_004
"""

from common.SwapServiceWS import t as swap_service_ws
from common.SwapServiceAPI import t as swap_api
from common.SwapServiceOrder import t as swap_order
from tool import atp
from pprint import pprint
import pytest, allure, random, time

@allure.epic('反向永续')  # 这里填业务线
@allure.feature('WS订阅')  # 这里填功能
@allure.story('BBO')  # 这里填子功能，没有的话就把本行注释掉
@pytest.mark.stable
@allure.tag('Script owner : 余辉青', 'Case owner : 吉龙')
class TestSwapNoti_004:

    @allure.step('前置条件')
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, contract_code, lever_rate, offsetO, offsetC, directionB, directionS):
        print("\n清盘》》》》", atp.ATP.clean_market())
        self.contract_code = contract_code
        self.lever_rate = lever_rate
        self.offsetO = offsetO
        self.offsetC = offsetC
        self.directionB = directionB
        self.directionS = directionS
        self.order_price_type = 'limit'
        self.currentPrice = atp.ATP.get_current_price()  # 最新价
        print('挂单，更新盘口深度')
        swap_api.swap_order(contract_code=self.contract_code, price=round(self.currentPrice * (1 - 0.01), 2),
                            order_price_type=self.order_price_type,
                            lever_rate=self.lever_rate, direction=self.directionB, offset=self.offsetO, volume=10)

        swap_api.swap_order(contract_code=self.contract_code, price=round(self.currentPrice * (1 + 0.01), 2),
                            order_price_type=self.order_price_type,
                            lever_rate=self.lever_rate, direction=self.directionS, offset=self.offsetO, volume=10)
        # 等待成交刷新最新价
        time.sleep(3)

    @allure.title('WS订阅BBO(单个合约，即传参合约code)')
    @allure.step('测试执行')
    def test_execute(self):
        with allure.step('WS订阅BBO(单个合约，即传参合约code)，可参考文档：https://docs.huobigroup.com/docs/coin_margined_swap/v1/cn/#websocket-3'):
            subs = {
                "sub": "market.{}.bbo".format(self.contract_code),
                "id": "id8"
            }
            result = swap_service_ws.swap_sub(subs)
            resultStr = '\n返回结果 = ' + str(result)
            print('\033[1;32;49m%s\033[0m' % resultStr)
            assert result['tick']['bid'] is not None
            assert result['tick']['ask'] is not None
            pass

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')


if __name__ == '__main__':
    pytest.main()
