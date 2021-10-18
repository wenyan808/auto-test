#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20211012
# @Author : 张广南
    用例标题
        restful请求深度  step13
    前置条件
        
    步骤/文本
        详见官方文档
    预期结果
        
    优先级
        0
    用例别名
        TestLinearNoti_restful_depth_014
"""

from common.LinearServiceAPI import t as linear_api
import pytest, allure, random, time
from tool import atp

@allure.epic('正向永续')  # 这里填业务线
@allure.feature('行情')  # 这里填功能
@allure.story('深度')  # 这里填子功能，没有的话就把本行注释掉
@pytest.mark.stable
@allure.tag('Script owner : 张广南', 'Case owner : 吉龙')
class TestLinearNoti_restful_depth_014:

    @allure.step('前置条件')
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, contract_code, lever_rate, offsetO, directionB, directionS):
        print("\n清盘》》》》", atp.ATP.clean_market())

        lever_rate = 5

        # 获取交割合约当前价格
        sell_price = atp.ATP.get_adjust_price(rate=1.01)
        buy_price = atp.ATP.get_adjust_price(rate=0.99)

        print('下两单，更新盘口数据')
        linear_api.linear_order(contract_code=contract_code, price=buy_price, volume='1', direction=directionB,
                                offset=offsetO, lever_rate=lever_rate, order_price_type='limit')
        linear_api.linear_order(contract_code=contract_code, price=sell_price, volume='1', direction=directionS,
                                offset=offsetO, lever_rate=lever_rate, order_price_type='limit')

        # 等待深度信息更新
        time.sleep(3)

    @allure.title('restful请求深度  step13')
    @allure.step('测试执行')
    def test_execute(self, contract_code):
        with allure.step('参考官方文档'):
            depth_type = 'step13'
            result = linear_api.linear_depth(contract_code=contract_code, type=depth_type)
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
