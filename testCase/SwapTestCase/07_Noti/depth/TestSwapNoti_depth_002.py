#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20211012
# @Author : 张广南
    用例标题
        WS订阅深度 150档step1
    前置条件
        
    步骤/文本
        参考官方文档
    预期结果
        订阅成功，数据正常
    优先级
        0
    用例别名
        TestSwapNoti_depth_002
"""

from common.SwapServiceAPI import t as swap_api
from common.SwapServiceWS import t as swap_service_ws
import pytest, allure, random, time

from tool import atp

@allure.epic('反向永续')  # 这里填业务线
@allure.feature('行情')  # 这里填功能
@allure.story('深度')  # 这里填子功能，没有的话就把本行注释掉
@pytest.mark.stable
@allure.tag('Script owner : 张广南', 'Case owner : 吉龙')
class TestSwapNoti_depth_002:

    @allure.step('前置条件')
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, contract_code, lever_rate, offsetO, directionB, directionS):
        print("\n清盘》》》》", atp.ATP.clean_market())

        lever_rate = 5

        # 获取交割合约当前价格
        sell_price = atp.ATP.get_adjust_price(rate=1.01)
        buy_price = atp.ATP.get_adjust_price(rate=0.99)

        print('下两单，更新盘口数据')
        swap_api.swap_order(contract_code=contract_code, price=buy_price, volume='1', direction=directionB,
                            offset=offsetO, lever_rate=lever_rate, order_price_type='limit')
        swap_api.swap_order(contract_code=contract_code, price=sell_price, volume='1', direction=directionS,
                            offset=offsetO, lever_rate=lever_rate, order_price_type='limit')

        # 等待深度信息更新
        time.sleep(3)

    @allure.title('WS订阅深度 150档step1')
    @allure.step('测试执行')
    def test_execute(self, contract_code):
        with allure.step('参考官方文档'):
            depth_type = 'step1'
            subs = {
                "sub": "market.{}.depth.{}".format(contract_code, depth_type),
                "id": "id5"
            }
            result = swap_service_ws.swap_sub(subs)
            result_str = '\nDepth返回结果 = ' + str(result)
            print('\033[1;32;49m%s\033[0m' % result_str)
            assert result['tick']['bids'] is not None
            assert result['tick']['asks'] is not None

    @allure.step('恢复环境')
    def teardown(self):
        atp.ATP.cancel_all_types_order()
        print('\n恢复环境操作')


if __name__ == '__main__':
    pytest.main()
