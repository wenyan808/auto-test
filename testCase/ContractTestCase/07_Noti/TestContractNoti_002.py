#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20211009
# @Author : 
    用例标题
        WS订阅深度(150档不合并，即传参step0)
    前置条件
        
    步骤/文本
        WS订阅深度(150档不合并，即传参step0)，可参考文档：https://docs.huobigroup.com/docs/dm/v1/cn/#websocket-3
    预期结果
        asks,bids 数据正确,不存在Null,[]
    优先级
        0
    用例别名
        TestContractNoti_002
"""

from common.ContractServiceAPI import t as contract_api
from common.ContractServiceOrder import t as contract_order
from common.ContractServiceWS import t as contract_service_ws

from pprint import pprint
import pytest
import allure
import random
import time
from tool import atp
from tool.atp import ATP


@allure.epic('反向交割')  # 这里填业务线
@allure.feature('订阅')  # 这里填功能
@allure.story('150档不合并深度')  # 这里填子功能，没有的话就把本行注释掉
@pytest.mark.stable
@allure.tag('Script owner : 余辉青', 'Case owner : 吉龙')
class TestContractNoti_002:

    @allure.step('前置条件')
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, symbol, symbol_period, lever_rate, directionB, directionS, offsetC, offsetO):
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
        print(self.symbol_period, '最新价 = ', self.currentPrice,
              ' 触发价 = ', self.highPrice, '买入价 = ', self.lowPrice)

        # 获取交割合约信息
        contractInfo = contract_api.contract_contract_info(
            symbol=symbol, contract_type=self.contract_type)
        print(self.symbol, '合约信息 = ', contractInfo)
        contract_code = contractInfo['data'][0]['contract_code']

        print('挂单，更新盘口深度')
        contract_api.contract_order(symbol=symbol, contract_type=self.contract_type, contract_code=contract_code,
                                    client_order_id=None, price=self.lowPrice, volume=1, direction=self.directionB,
                                    offset=self.offsetO,
                                    lever_rate=lever_rate, order_price_type=self.order_price_type)
        contract_api.contract_order(symbol=symbol, contract_type=self.contract_type, contract_code=contract_code,
                                    client_order_id=None, price=self.highPrice, volume=1, direction=self.directionS,
                                    offset=self.offsetO,
                                    lever_rate=self.lever_rate, order_price_type=self.order_price_type)

        # 等待深度信息更新
        time.sleep(3)

    @allure.title('WS订阅深度(150档不合并，即传参step0)')
    @allure.step('测试执行')
    def test_execute(self, symbol, symbol_period):
        with allure.step('WS订阅深度(150档不合并，即传参step0)，可参考文档：https://docs.huobigroup.com/docs/dm/v1/cn/#websocket-3'):
            self.depthType = 'step0'
            subs = {
                "sub": "market.{}.depth.{}".format(self.symbol_period, self.depthType),
                "id": "id5"
            }
            result = contract_service_ws.contract_sub(subs)
            resultStr = '\nDepth返回结果 = ' + str(result)
            print('\033[1;32;49m%s\033[0m' % resultStr)
            if 'tick' in result:
                if not result['tick']['bids']:
                    assert False
                if not result['tick']['asks']:
                    assert False

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')
        ATP.cancel_all_order()


if __name__ == '__main__':
    pytest.main()
