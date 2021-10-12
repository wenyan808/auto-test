#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20211012
# @Author : 张广南
    用例标题
        WS订阅深度 20档step9
    前置条件
        
    步骤/文本
        参考官方文档
    预期结果
        订阅成功，数据正常
    优先级
        0
    用例别名
        TestContractNoti_depth_012
"""

from common.ContractServiceAPI import t as contract_api
from common.ContractServiceWS import t as contract_service_ws

from pprint import pprint
import pytest, allure, random, time
from tool import atp

@allure.epic('反向交割')  # 这里填业务线
@allure.feature('行情')  # 这里填功能
@allure.story('深度')  # 这里填子功能，没有的话就把本行注释掉
@pytest.mark.stable
class TestContractNoti_depth_012:

    @allure.step('前置条件')
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, symbol_period):
        print("\n清盘》》》》", atp.ATP.clean_market())
        contract_types = {'CW': "this_week", 'NW': "next_week", 'CQ': "quarter", 'NQ': "next_quarter"}
        symbol = symbol_period.split('_')[0]
        contract_type = contract_types[symbol_period.split('_')[1]]
        lever_rate = 5

        # 获取交割合约当前价格
        sell_price = atp.ATP.get_adjust_price(rate=1.01)
        buy_price = atp.ATP.get_adjust_price(rate=0.99)

        contractInfo = contract_api.contract_contract_info(symbol=symbol, contract_type=contract_type)
        print('BTC当周合约信息 = ', contractInfo)
        contract_code = contractInfo['data'][0]['contract_code']

        print('下两单，更新Kline数据')
        contract_api.contract_order(symbol=symbol, contract_type=contract_type, price=str(buy_price), volume='1',
                                    direction='buy', offset='open', lever_rate=lever_rate, order_price_type='limit')
        contract_api.contract_order(symbol=symbol, contract_type=contract_type, price=str(sell_price), volume='1',
                                    direction='sell', offset='open', lever_rate=lever_rate, order_price_type='limit')

        # 等待深度信息更新
        time.sleep(3)

    @allure.title('WS订阅深度(150档不合并，即传参step0)')
    @allure.step('测试执行')
    def test_execute(self, symbol, symbol_period):
        with allure.step('WS订阅深度(150档不合并，即传参step0)，可参考文档：https://docs.huobigroup.com/docs/dm/v1/cn/#websocket-3'):
            depth_type = 'step9'
            result = contract_service_ws.contract_sub_depth(contract_code=symbol_period, type=depth_type)
            result_str = '\nDepth返回结果 = ' + str(result)
            print('\033[1;32;49m%s\033[0m' % result_str)
            if not result['tick']['bids']:
                assert False
            if not result['tick']['asks']:
                assert False
            pass

    @allure.step('恢复环境')
    def teardown(self):
        atp.ATP.cancel_all_types_order()
        print('\n恢复环境操作')


if __name__ == '__main__':
    pytest.main()
