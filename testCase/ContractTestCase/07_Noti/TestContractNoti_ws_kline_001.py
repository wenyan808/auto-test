#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20211012
# @Author : 
    用例标题
        WS订阅K线(req 传参from,to)
    前置条件
        
    步骤/文本
        详见官方文档
    预期结果
        id、open、close、low、high价格正确；amount、vol、count值正确,不存在Null,[]
    优先级
        0
    用例别名
        TestContractNoti_ws_kline_001
"""

from common.ContractServiceAPI import t as contract_api
from common.ContractServiceOrder import t as contract_order
from common.ContractServiceWS import t as contract_service_ws
from pprint import pprint
import pytest, allure, random, time
from tool import atp

@allure.epic('反向交割')  # 这里填业务线
@allure.feature('WS订阅')  # 这里填功能
@allure.story('请求K线数据-1min')  # 这里填子功能，没有的话就把本行注释掉
@pytest.mark.stable
@allure.tag('Script owner : 余辉青', 'Case owner : 吉龙')
class TestContractNoti_ws_kline_001:

    @allure.step('前置条件')
    @pytest.fixture(scope='function', autouse=True)
    def setup(self,symbol,symbol_period):
        self.symbol = symbol
        self.contract_code = symbol_period
        self.period = '1min'

    @allure.title('WS订阅K线(req 传参from,to)')
    @allure.step('测试执行')
    def test_execute(self):
        with allure.step('详见官方文档'):
            # "BTC_CW"    表示BTC当周合约
            # "BTC_NW"    表示BTC次周合约
            # "BTC_CQ"    表示BTC当季合约
            # "BTC_NQ"    表示BTC次季度合约
            toTime = int(time.time())
            fromTime = toTime - 60*5
            subs = {
                "req": "market.{}.kline.{}".format(self.contract_code, self.period),
                "id": "id4",
                "from": fromTime,
                "to": toTime
            }
            result = contract_service_ws.contract_sub(subs=subs)
            resultStr = '\nKline返回结果 = ' + str(result)
            print('\033[1;32;49m%s\033[0m' % resultStr)

            # data为空判定失败
            if not result['data']:
                assert False

            pass

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')


if __name__ == '__main__':
    pytest.main()
