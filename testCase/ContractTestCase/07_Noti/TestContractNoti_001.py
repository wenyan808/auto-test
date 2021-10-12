#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20211009
# @Author : 
    用例标题
        WS订阅K线(传参from,to)
    前置条件
        
    步骤/文本
        WS订阅K线(传参from,to)，可参考文档：https://docs.huobigroup.com/docs/dm/v1/cn/#websocket-3
    预期结果
        id、open、close、low、high价格正确；amount、vol、count值正确,不存在Null,[]
    优先级
        0
    用例别名
        TestContractNoti_001
"""

from common.ContractServiceAPI import t as contract_api
from common.ContractServiceOrder import t as contract_order
from common.ContractServiceWS import t as contract_service_ws
from pprint import pprint
import pytest, allure, random, time
from tool import atp

@allure.epic('反向交割')  # 这里填业务线
@allure.feature('WS订阅')  # 这里填功能
@allure.story('订阅K线')  # 这里填子功能，没有的话就把本行注释掉
@pytest.mark.stable
class TestContractNoti_001:

    @allure.step('前置条件')
    def setup(self):
        print("\n清卖盘》》》》", atp.ATP.clean_market(contract_code='BTC_CW', direction='sell'))
        print("\n清买盘》》》》", atp.ATP.clean_market(contract_code='BTC_CW', direction='buy'))

        lever_rate = 5
        symbol = 'BTC'

        contract_type = 'this_week'
        order_price_type = 'limit'
        offset = 'open'
        low = '45000'
        high = '50000'
        buy = 'buy'
        sell = 'sell'

        # 获取交割合约信息
        contractInfo = contract_api.contract_contract_info(symbol=symbol, contract_type=contract_type)
        print('BTC当周合约信息 = ', contractInfo)
        contract_code = contractInfo['data'][0]['contract_code']

        print('进行2笔交易，更新Kline数据')
        contract_api.contract_order(symbol=symbol, contract_type=contract_type, contract_code=contract_code,
                       client_order_id=None, price=low, volume=1, direction=buy, offset=offset,
                       lever_rate=lever_rate, order_price_type=order_price_type)

        contract_api.contract_order(symbol=symbol, contract_type=contract_type, contract_code=contract_code,
                       client_order_id=None, price=low, volume=1, direction=sell, offset=offset,
                       lever_rate=lever_rate, order_price_type=order_price_type)
        # 等待成交刷新最新价
        time.sleep(1)
        contract_api.contract_order(symbol=symbol, contract_type=contract_type, contract_code=contract_code,
                       client_order_id=None, price=high, volume=1, direction=buy, offset=offset,
                       lever_rate=lever_rate, order_price_type=order_price_type)
        contract_api.contract_order(symbol=symbol, contract_type=contract_type, contract_code=contract_code,
                       client_order_id=None, price=high, volume=1, direction=sell, offset=offset,
                       lever_rate=lever_rate, order_price_type=order_price_type)
        # 等待成交刷新最新价
        time.sleep(1)

    @allure.title('WS订阅K线(传参from,to)')
    @allure.step('测试执行')
    def test_execute(self):
        with allure.step('WS订阅K线(传参from,to)，可参考文档：https://docs.huobigroup.com/docs/dm/v1/cn/#websocket-3'):
            # "BTC_CW"    表示BTC当周合约
            # "BTC_NW"    表示BTC次周合约
            # "BTC_CQ"    表示BTC当季合约
            # "BTC_NQ"    表示BTC次季度合约
            contractCode = 'BTC_CW'
            low = 45000
            high = 50000
            period = '1min'
            result = contract_service_ws.contract_sub_kline(contract_code=contractCode, period=period)
            resultStr = '\nKline返回结果 = ' + str(result)
            print('\033[1;32;49m%s\033[0m' % resultStr)
            # 最低价校验,避免测试执行期间有更低价的成交影响断言
            if result['tick']['low'] > low:
                assert False
            # 最高价校验,避免测试执行期间有更高价的成交影响断言
            if result['tick']['high'] < high:
                assert False
            # 收仓价校验
            if result['tick']['close']  !=high:
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
