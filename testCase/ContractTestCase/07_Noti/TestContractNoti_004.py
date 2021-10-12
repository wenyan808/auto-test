#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20211009
# @Author : 
    用例标题
        WS订阅BBO(单个合约，即传参合约code)
    前置条件
        
    步骤/文本
        WS订阅BBO(单个合约，即传参合约code)，可参考文档：https://docs.huobigroup.com/docs/dm/v1/cn/#websocket-3
    预期结果
        asks,bids 数据正确,不存在Null,[]
    优先级
        0
    用例别名
        TestContractNoti_004
"""
from common.ContractServiceAPI import t as contract_api
from common.ContractServiceOrder import t as contract_order
from common.ContractServiceWS import t as contract_service_ws
from pprint import pprint
import pytest, allure, random, time
from tool import atp

@allure.epic('反向交割')  # 这里填业务线
@allure.feature('订阅')  # 这里填功能
@allure.story('BBO')  # 这里填子功能，没有的话就把本行注释掉
@pytest.mark.stable
class TestContractNoti_004:

    @allure.step('前置条件')
    def setup(self):
        print("\n清卖盘》》》》", atp.ATP.clean_market(contract_code='BTC_CW', direction='sell'))
        print("\n清买盘》》》》", atp.ATP.clean_market(contract_code='BTC_CW', direction='buy'))
        lever_rate = 5
        symbol = 'BTC'
        contract_type = 'this_week'
        order_price_type = 'limit'
        offset = 'open'
        buy = 'buy'
        sell = 'sell'

        # 获取交割合约信息
        contractInfo = contract_api.contract_contract_info(symbol=symbol, contract_type=contract_type)
        print('BTC当周合约信息 = ', contractInfo)
        contract_code = contractInfo['data'][0]['contract_code']

        print('进行2笔交易，更新Kline数据')
        contract_api.contract_order(symbol=symbol, contract_type=contract_type, contract_code=contract_code,
                                    client_order_id=None, price='45000', volume=1, direction=buy, offset=offset,
                                    lever_rate=lever_rate, order_price_type=order_price_type)

        contract_api.contract_order(symbol=symbol, contract_type=contract_type, contract_code=contract_code,
                                    client_order_id=None, price='45001', volume=1, direction=sell, offset=offset,
                                    lever_rate=lever_rate, order_price_type=order_price_type)
        # 等待深度信息更新
        time.sleep(3)

    @allure.title('WS订阅BBO(单个合约，即传参合约code)')
    @allure.step('测试执行')
    def test_execute(self, symbol, symbol_period):
        with allure.step('WS订阅BBO(单个合约，即传参合约code)，可参考文档：https://docs.huobigroup.com/docs/dm/v1/cn/#websocket-3'):
            contractCode = 'BTC_CW'
            result = contract_service_ws.contract_sub_bbo(contract_code=contractCode)
            resultStr = '\nDepth返回结果 = ' + str(result)
            print('\033[1;32;49m%s\033[0m' % resultStr)
            if not result['tick']['bid']:
                assert False
            if not result['tick']['ask']:
                assert False
            pass

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')


if __name__ == '__main__':
    pytest.main()
