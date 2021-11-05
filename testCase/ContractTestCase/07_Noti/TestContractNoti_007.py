#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20211009
# @Author : chenwei
    用例标题
        WS订阅最新成交记录(单个合约，即传参contract_code)
    前置条件
        
    步骤/文本
        WS订阅最新成交记录(单个合约，即传参contract_code)，可参考文档：https://docs.huobigroup.com/docs/dm/v1/cn/#websocket-3
    预期结果
        amount\quantity\turnover\direction\price显示正确,不存在Null,[]
    优先级
        0
    用例别名
        TestContractNoti_007
"""

from common.ContractServiceAPI import t as contract_api,ContractServiceAPI
from common.ContractServiceOrder import t as contract_order
from common.LinearServiceAPI import t as linear_api
from common.LinearServiceOrder import t as linear_order
from common.SwapServiceAPI import t as swap_api
from common.SwapServiceOrder import t as swap_order

from pprint import pprint
import pytest, allure, random, time
from tool.atp import ATP
from common.ContractServiceWS import t as websocketsevice
from config.conf import COMMON_ACCESS_KEY, COMMON_SECRET_KEY, URL
from tool.atp import ATP

@allure.epic('反向交割')  # 这里填业务线
@allure.feature('WS订阅')  # 这里填功能
@allure.story('行情')  # 这里填子功能，没有的话就把本行注释掉
@pytest.mark.stable
@allure.tag('Script owner : chenwei', 'Case owner : 吉龙')
class TestContractNoti_007:

    @allure.step('前置条件')
    def setup(self):
        print('''  ''')
        print('''  ''')
        ATP.close_all_position()
        print(''' 使当前交易对有交易盘口  ''')
        print(ATP.make_market_depth())
        print(''' 使当前用户有持仓  ''')

    @allure.title('WS订阅最新成交记录(单个合约，即传参contract_code)')
    @allure.step('测试执行')
    def test_execute(self, symbol, symbol_period):
        leverrate = '5'
        print('\n获取最近价\n')
        r = contract_api.contract_history_trade(symbol=symbol_period, size='1')
        pprint(r)
        # 得到最近的价格
        lastprice = r['data'][0]['data'][0]['price']
        sellprice = round((lastprice * 0.98), 2)
        print('\n下一个卖单\n')
        r = contract_api.contract_order(symbol=symbol,
                                    contract_type='this_week',
                                    price=sellprice,
                                    volume='1',
                                    direction='sell',
                                    offset='open',
                                    lever_rate=leverrate,
                                    order_price_type='limit')
        pprint(r)
        print('\n下一个买单\n')
        buyprice = round((lastprice * 1.02), 2)
        service = ContractServiceAPI(URL, COMMON_ACCESS_KEY, COMMON_SECRET_KEY)
        r = service.contract_order(symbol=symbol,
                                    contract_type='this_week',
                                    price=buyprice,
                                    volume='1',
                                    direction='buy',
                                    offset='open',
                                    lever_rate=leverrate,
                                    order_price_type='limit')
        pprint(r)
        time.sleep(2)
        with allure.step('WS订阅最新成交记录(单个合约，即传参contract_code)，可参考文档：https://docs.huobigroup.com/docs/dm/v1/cn/#websocket-3'):
            r = contract_api.contract_depth(symbol=symbol_period, type="step0")
            pprint(r)
            r = websocketsevice.contract_sub_trade_detail(symbol=symbol_period)
            pprint(r)
            tradedetail = r['tick']['data'][0]
            if tradedetail['amount'] == None:
                assert False
            if tradedetail['direction'] == None:
                assert False
            if tradedetail['price'] == None:
                assert False
            if tradedetail['quantity'] == None:
                assert False

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')
        ATP.cancel_all_order()


if __name__ == '__main__':
    pytest.main()
