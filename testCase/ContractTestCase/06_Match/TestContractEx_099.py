#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20211028
# @Author : 
    用例标题
        撮合当周 买入平仓 全部成交单人多笔价格相同的订单     
    前置条件
        
    步骤/文本
        详见官方文档
    预期结果
        正确撮合
    优先级
        2
    用例别名
        TestContractEx_099
"""

from common.ContractServiceAPI import t as contract_api
from common.ContractServiceOrder import t as contract_order
from common.LinearServiceAPI import t as linear_api
from common.LinearServiceOrder import t as linear_order
from common.SwapServiceAPI import t as swap_api
from common.SwapServiceOrder import t as swap_order

from pprint import pprint
import pytest
import allure
import random
import time
from tool.atp import ATP
from common.mysqlComm import orderSeq as DB_orderSeq


@allure.epic('反向交割')  # 这里填业务线
@allure.feature('撮合')  # 这里填功能
@allure.story('委托单')  # 这里填子功能，没有的话就把本行注释掉
@pytest.mark.stable
@allure.tag('Script owner : chenwei', 'Case owner : 邱大伟')
class TestContractEx_099:

    @allure.step('前置条件')
    def setup(self):
        print(''' 制造成交数据 ''')
        ATP.make_market_depth(depth_count=5)
        sell_price = ATP.get_adjust_price(1.02)
        buy_price = ATP.get_adjust_price(0.98)
        ATP.common_user_make_order(price=sell_price, direction='sell')
        ATP.common_user_make_order(price=buy_price, direction='buy')
        time.sleep(1)

    @allure.title('撮合当周 买入平仓 全部成交单人多笔价格相同的订单     ')
    @allure.step('测试执行')
    def test_execute(self, symbol, symbol_period):
        with allure.step('详见官方文档'):
            contracttype = 'this_week'
            leverrate = 5
            current = ATP.get_current_price(contract_code=symbol_period)

            res = ATP.current_user_make_order(
                contract_code=symbol_period, price=current, volume=5, direction="sell", offset="close")
            pprint(res)
            time.sleep(2)
            buy_order = contract_api.contract_order(symbol=symbol, contract_type=contracttype, price=current,
                                                    volume=2,
                                                    direction="buy", offset='close', lever_rate=leverrate,
                                                    order_price_type='limit')
            pprint(buy_order)
            time.sleep(2)
            buy_order1 = contract_api.contract_order(symbol=symbol, contract_type=contracttype, price=current,
                                                     volume=3,
                                                     direction="buy", offset='close', lever_rate=leverrate,
                                                     order_price_type='limit')

            pprint(buy_order1)
            orderId = buy_order1['data']['order_id']
            time.sleep(2)
            strStr = "select count(1) from t_exchange_match_result WHERE f_id = " \
                     "(select f_id from t_order_sequence where f_order_id= '%s')" % (
                         orderId)

            # 给撮合时间，5秒内还未撮合完成则为失败
            n = 0
            while n < 5:
                isMatch = DB_orderSeq.execute(strStr)[0][0]
                if 1 == isMatch:
                    break
                else:
                    n = n + 1
                    time.sleep(1)
                    print('等待处理，第' + str(n) + '次重试………………………………')
                    if n == 5:
                        assert False

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')
        ATP.cancel_all_types_order()


if __name__ == '__main__':
    pytest.main()
