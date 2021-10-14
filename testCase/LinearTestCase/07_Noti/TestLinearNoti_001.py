#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20211008
# @Author : YuHuiQing
    用例标题
        请求K线(传参from,to)
    前置条件
        
    步骤/文本
        请求K线(传参from,to)，可参考文档：https://docs.huobigroup.com/docs/usdt_swap/v1/cn/#websocket-3
    预期结果
        id、open、close、low、high价格正确；amount、vol、count值正确,不存在Null,[]
    优先级
        
    用例别名
        restful请求
"""

import allure
import pytest
import time

from common.LinearServiceAPI import t as linear_api
from common.LinearServiceWS import t as linear_service_ws
from tool import atp
from tool.atp import ATP


@allure.epic('正向永续')  # 这里填业务线
@allure.feature('WS订阅')  # 这里填功能
@allure.story('订阅Kline')  # 这里填子功能，没有的话就把本行注释掉
@pytest.mark.stable
@allure.tag('Script owner : 余辉青', 'Case owner : 吉龙')
class TestLinearNoti_001:

    @allure.step('前置条件')
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, contract_code, lever_rate, offsetO, directionB, directionS):
        ATP.clean_market()
        time.sleep(2)
        self.lever_rate = lever_rate
        self.contract_code = contract_code
        self.order_price_type = 'limit'
        self.offsetO = offsetO
        self.currentPrice = atp.ATP.get_current_price()  # 最新价
        self.lowPrice = round(self.currentPrice * 0.09, 2)  # 买入价
        self.highPrice = round(self.currentPrice * 1.01, 2)  # 触发价
        self.directionB = directionB
        self.directionS = directionS
        print('进行2笔交易，更新Kline数据')
        linear_api.linear_order(contract_code=self.contract_code, price=self.lowPrice,
                                order_price_type=self.order_price_type,
                                lever_rate=self.lever_rate, direction=self.directionB, offset=self.offsetO, volume=1)

        linear_api.linear_order(contract_code=self.contract_code, price=self.lowPrice,
                                order_price_type=self.order_price_type,
                                lever_rate=self.lever_rate, direction=self.directionS, offset=self.offsetO, volume=1)
        # 等待成交刷新最新价
        time.sleep(1)
        linear_api.linear_order(contract_code=self.contract_code, price=self.highPrice,
                                order_price_type=self.order_price_type,
                                lever_rate=self.lever_rate, direction=self.directionB, offset=self.offsetO, volume=1)

        linear_api.linear_order(contract_code=self.contract_code, price=self.highPrice,
                                order_price_type=self.order_price_type,
                                lever_rate=self.lever_rate, direction=self.directionS, offset=self.offsetO, volume=1)
        # 等待成交刷新最新价
        time.sleep(1)

    @allure.title('请求K线(传参from,to)')
    @allure.step('测试执行')
    def test_execute(self):
        with allure.step('1、订阅Kline获取订阅结果'):
            self.period = '1min'
            result = linear_service_ws.linear_sub_kline(contract_code=self.contract_code, period=self.period)
            resultStr = '\nKline返回结果 = ' + str(result)
            print('\033[1;32;49m%s\033[0m' % resultStr)
            # 最低价校验
            if result['tick']['low'] != self.lowPrice:
                assert False
            # 最高价校验
            if result['tick']['high'] != self.highPrice:
                assert False
            # 收仓价校验
            if result['tick']['close'] != self.highPrice:
                assert False
            # 成交额, 即sum（每一笔成交张数 * 合约面值 * 成交价格）。 值是买卖双边之和
            if result['tick']['trade_turnover'] == 0:
                assert False
            # 成交量张数。 值是买卖双边之和
            if result['tick']['vol'] < 4:
                assert False
            # 成交笔数。 值是买卖双边之和
            if result['tick']['count'] < 2:
                assert False
            pass

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')


if __name__ == '__main__':
    pytest.main()
