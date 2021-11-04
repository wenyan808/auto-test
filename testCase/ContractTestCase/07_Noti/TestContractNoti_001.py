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
from tool.atp import ATP

@allure.epic('反向交割')  # 这里填业务线
@allure.feature('WS订阅')  # 这里填功能
@allure.story('订阅K线')  # 这里填子功能，没有的话就把本行注释掉
@pytest.mark.stable
@allure.tag('Script owner : 余辉青', 'Case owner : 吉龙')
class TestContractNoti_001:

    @allure.step('前置条件')
    @pytest.fixture(scope='function', autouse=True)
    def setup(self,symbol,symbol_period,lever_rate,directionB,directionS,offsetC,offsetO):
        print("\n清盘》》》》", atp.ATP.clean_market())
        self.lever_rate = lever_rate
        self.symbol = symbol
        self.symbol_period = symbol_period
        # "BTC_CW"    表示BTC当周合约
        # "BTC_NW"    表示BTC次周合约
        # "BTC_CQ"    表示BTC当季合约
        # "BTC_NQ"    表示BTC次季度合约
        if '_CW' in self.symbol_period:
            self.contract_type = 'this_week'
        elif '_NW' in self.symbol_period:
            self.contract_type = 'next_week'
        elif '_CQ' in self.symbol_period:
            self.contract_type = 'quarter'
        elif '_NQ' in self.symbol_period:
            self.contract_type = 'next_quarter'

        self.order_price_type = 'limit'
        self.offsetO = offsetO
        self.offsetC = offsetC
        self.directionB = directionB
        self.directionS = directionS
        self.currentPrice = atp.ATP.get_current_price()  # 最新价
        self.lowPrice = round(self.currentPrice * 0.99, 2)  # 买入价
        self.highPrice = round(self.currentPrice * 1.01, 2)  # 触发价
        print(self.symbol_period, '最新价 = ', self.currentPrice, ' 触发价 = ', self.highPrice, '买入价 = ', self.lowPrice)

        # 获取交割合约信息
        contractInfo = contract_api.contract_contract_info(symbol=symbol, contract_type=self.contract_type)
        print(self.symbol,'合约信息 = ', contractInfo)
        contract_code = contractInfo['data'][0]['contract_code']

        print('进行2笔交易，更新Kline数据')
        contract_api.contract_order(symbol=symbol, contract_type=self.contract_type, contract_code=contract_code,
                       client_order_id=None, price=self.lowPrice, volume=1, direction=self.directionB, offset=self.offsetO,
                       lever_rate=lever_rate, order_price_type=self.order_price_type)
        contract_api.contract_order(symbol=symbol, contract_type=self.contract_type, contract_code=contract_code,
                       client_order_id=None, price=self.lowPrice, volume=1, direction=self.directionS, offset=self.offsetO,
                       lever_rate=self.lever_rate, order_price_type=self.order_price_type)
        # 等待成交刷新最新价
        time.sleep(1)
        contract_api.contract_order(symbol=symbol, contract_type=self.contract_type, contract_code=contract_code,
                                    client_order_id=None, price=self.highPrice, volume=1, direction=self.directionB,
                                    offset=self.offsetO,
                                    lever_rate=lever_rate, order_price_type=self.order_price_type)
        contract_api.contract_order(symbol=symbol, contract_type=self.contract_type, contract_code=contract_code,
                                    client_order_id=None, price=self.highPrice, volume=1, direction=self.directionS,
                                    offset=self.offsetO,
                                    lever_rate=self.lever_rate, order_price_type=self.order_price_type)
        # 等待成交刷新最新价
        time.sleep(1)

    @allure.title('WS订阅K线(传参from,to)')
    @allure.step('测试执行')
    def test_execute(self):
        with allure.step('WS订阅K线(传参from,to)，可参考文档：https://docs.huobigroup.com/docs/dm/v1/cn/#websocket-3'):
            self.period = '1min'
            subs = {
                "sub": "market.{}.kline.{}".format(self.symbol_period, self.period),
                "id": "id1"
            }
            result = contract_service_ws.contract_sub(subs=subs)
            resultStr = '\nKline返回结果 = ' + str(result)
            print('\033[1;32;49m%s\033[0m' % resultStr)
            # 最低价校验,避免测试执行期间有更低价的成交影响断言
            if result['tick']['low'] > self.lowPrice:
                assert False
            # 最高价校验,避免测试执行期间有更高价的成交影响断言
            if result['tick']['high'] < self.highPrice:
                assert False
            # 收仓价校验
            if result['tick']['close']  !=self.highPrice:
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
        ATP.clean_market()
        ATP.cancel_all_order()


if __name__ == '__main__':
    pytest.main()
