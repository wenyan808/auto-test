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

from common.ContractServiceAPI import t as contract_api
from common.ContractServiceOrder import t as contract_order
from common.LinearServiceAPI import t as linear_api
from common.LinearServiceOrder import t as linear_order
from common.SwapServiceAPI import t as swap_api
from common.SwapServiceOrder import t as swap_order
from common.LinearServiceWS import t as linear_service_ws
import json
from pprint import pprint
import pytest, allure, random, time


@allure.epic('正向永续')  # 这里填业务线
@allure.feature('WS订阅')  # 这里填功能
@allure.story('订阅Kline')  # 这里填子功能，没有的话就把本行注释掉
class TestLinearNoti_010:

    @allure.step('前置条件')
    def setup(self):
        lever_rate = 5
        contractCode = 'BTC-USDT'
        order_price_type = 'limit'
        offset = 'open'
        low = '45000'
        high = '50000'
        buy = 'buy'
        sell = 'sell'
        print('进行2笔交易，更新Kline数据')
        linear_api.linear_order(contract_code=contractCode, price= low, order_price_type=order_price_type, lever_rate=lever_rate,
                                direction=buy, offset=offset,
                                volume=1, )

        linear_api.linear_order(contract_code=contractCode, price= low, order_price_type=order_price_type, lever_rate=lever_rate,
                                direction=sell, offset=offset,
                                volume=1, )
        # 等待成交刷新最新价
        time.sleep(0.3)
        linear_api.linear_order(contract_code=contractCode, price=high, order_price_type=order_price_type,
                                lever_rate=lever_rate,
                                direction=buy, offset=offset,
                                volume=1, )
        linear_api.linear_order(contract_code=contractCode, price=high, order_price_type=order_price_type,
                                lever_rate=lever_rate,
                                direction=sell, offset=offset,
                                volume=1, )
        # 等待成交刷新最新价
        time.sleep(0.3)

    @allure.title('请求K线(传参from,to)')
    @allure.step('测试执行')
    def test_execute(self):
        with allure.step('1、订阅Kline获取订阅结果'):
            contractCode = 'BTC-USDT'
            low = 45000
            high = 50000
            period = '1min'
            result = linear_service_ws.linear_sub_kline(contract_code=contractCode,period=period)
            resultStr = '\nKline返回结果 = ' + str(result)
            print('\033[1;32;49m%s\033[0m' % resultStr)
            # 最低价校验
            if result['tick']['low'] != low:
                assert False
            # 最高价校验
            if result['tick']['high'] != high:
                assert False
            # 收仓价校验
            if result['tick']['close'] != high:
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
