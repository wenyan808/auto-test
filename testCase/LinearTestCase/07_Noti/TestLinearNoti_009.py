#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20211009
# @Author : chenwei
    用例标题
        WS订阅深度图
    前置条件
        
    步骤/文本
        WS订阅深度图，可参考文档：https://docs.huobigroup.com/docs/usdt_swap/v1/cn/#websocket-3
    预期结果
        asks,bids 数据正确,不存在Null,[]
    优先级
        0
    用例别名
        TestLinearNoti_009
"""

from common.ContractServiceAPI import t as contract_api
from common.ContractServiceOrder import t as contract_order
from common.LinearServiceAPI import t as linear_api
from common.LinearServiceOrder import t as linear_order
from common.SwapServiceAPI import t as swap_api
from common.SwapServiceOrder import t as swap_order

from pprint import pprint
import pytest, allure, random, time
from common.LinearServiceWS import t as websocketsevice
from tool.atp import ATP
@allure.epic('业务线')  # 这里填业务线
@allure.feature('功能')  # 这里填功能
@allure.story('子功能')  # 这里填子功能，没有的话就把本行注释掉
@pytest.mark.stable
class TestLinearNoti_009:

    @allure.step('前置条件')
    def setup(self):
        ATP.close_all_position()
        print(''' 使当前交易对有交易盘口  ''')
        print(ATP.make_market_depth())
        time.sleep(0.5)
        print(ATP.current_user_make_order(order_price_type='opponent'))

    @allure.title('WS订阅深度图')
    @allure.step('测试执行')
    def test_execute(self, contract_code):
        leverrate = '5'
        print('\n获取最近价\n')
        r = linear_api.linear_history_trade(contract_code=contract_code, size='1')
        pprint(r)
        # 得到最近的价格
        lastprice = r['data'][0]['data'][0]['price']
        sellprice = round((lastprice * 1.02), 2)
        print('\n下一个卖单\n')
        r = linear_api.linear_order(contract_code=contract_code,
                                    client_order_id='',
                                    price=sellprice,
                                    volume='1',
                                    direction='sell',
                                    offset='open',
                                    lever_rate=leverrate,
                                    order_price_type='limit')
        pprint(r)
        print('\n下一个买单\n')
        buyprice = round((lastprice * 0.98), 2)
        r = linear_api.linear_order(contract_code=contract_code,
                                    client_order_id='',
                                    price=buyprice,
                                    volume='1',
                                    direction='buy',
                                    offset='open',
                                    lever_rate=leverrate,
                                    order_price_type='limit')
        pprint(r)

        time.sleep(2)
        with allure.step('WS订阅深度图，可参考文档：https://docs.huobigroup.com/docs/usdt_swap/v1/cn/#websocket-3'):
            pprint("""api 获取行情深度数据""")
            r_trend_req = linear_api.linear_depth(contract_code=contract_code, type="step0")
            pprint(r_trend_req)
            pprint("""ws 获取行情深度数据""")
            n = 0
            while n<2:
                r = websocketsevice.linear_sub_depth(contract_code=contract_code,type="step0")
                pprint(r)
                n = n+1
            ask = r['tick']['asks'][0]
            bid = r['tick']['bids'][0]
            pprint(ask)
            pprint(bid)
            if ask == None:
                assert False
            if bid == None:
                assert False

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')
        ATP.cancel_all_trigger_order()
        ATP.cancel_all_order()
        ATP.close_all_position()


if __name__ == '__main__':
    pytest.main()
