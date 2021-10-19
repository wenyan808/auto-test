#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20211009
# @Author : 
    用例标题
        WS订阅深度(150档不合并，即传参step0)
    前置条件
        
    步骤/文本
        WS订阅深度(150档不合并，即传参step0)，可参考文档：https://docs.huobigroup.com/docs/usdt_swap/v1/cn/#websocket-3
    预期结果
        asks,bids 数据正确,不存在Null,[]
    优先级
        0
    用例别名
        TestLinearNoti_002
"""

from common.LinearServiceAPI import t as linear_api
from common.LinearServiceOrder import t as linear_order
from common.LinearServiceWS import t as linear_service_ws
import pytest, allure, random, time
from tool.atp import  ATP

@allure.epic('正向永续')  # 这里填业务线
@allure.feature('WS订阅')  # 这里填功能
@allure.story('WS订阅深度(150档不合并，即传参step0)')  # 这里填子功能，没有的话就把本行注释掉
@pytest.mark.stable
@allure.tag('Script owner : 余辉青', 'Case owner : 吉龙')
class TestLinearNoti_002:

    @allure.step('前置条件')
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, contract_code, lever_rate, offsetO, directionB, directionS):
        print("\n清盘》》》》", ATP.clean_market())

        lever_rate = 5

        # 获取交割合约当前价格
        sell_price = ATP.get_adjust_price(rate=1.01)
        buy_price = ATP.get_adjust_price(rate=0.99)

        print('下两单，更新盘口数据')
        linear_api.linear_order(contract_code=contract_code, price=buy_price, volume='1', direction=directionB,
                                offset=offsetO, lever_rate=lever_rate, order_price_type='limit')
        linear_api.linear_order(contract_code=contract_code, price=sell_price, volume='1', direction=directionS,
                                offset=offsetO, lever_rate=lever_rate, order_price_type='limit')

    @allure.title('WS订阅深度(150档不合并，即传参step0)')
    @allure.step('测试执行')
    def test_execute(self,contract_code):
        with allure.step('WS订阅深度(150档不合并，即传参step0)，可参考文档：https://docs.huobigroup.com/docs/usdt_swap/v1/cn/#websocket-3'):
            depthType = 'step0'
            subs = {
                "sub": "market.{}.depth.{}".format(contract_code,depthType),
                "id": "id5"
            }
            result = linear_service_ws.linear_sub(subs)
            result_str = '\nDepth返回结果 = ' + str(result)
            print('\033[1;32;49m%s\033[0m' % result_str)
            assert result['tick']['bids'] is not None
            assert result['tick']['asks'] is not None
            pass

    @allure.step('恢复环境')
    def teardown(self):
        print("")
if __name__ == '__main__':
    pytest.main()
