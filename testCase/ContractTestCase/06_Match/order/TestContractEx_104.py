#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20211028
# @Author : 
    用例标题
        撮合当周 卖出平仓 部分成交多人多笔价格相同的订单     
    前置条件
        
    步骤/文本
        详见官方文档
    预期结果
        正确撮合
    优先级
        2
    用例别名
        TestContractEx_104
"""

from pprint import pprint

import allure
import pytest
import time

from common.ContractServiceAPI import t as contract_api
from tool.atp import ATP


@allure.epic('反向交割')  # 这里填业务线
@allure.feature('撮合')  # 这里填功能
@allure.story('委托单')  # 这里填子功能，没有的话就把本行注释掉
@pytest.mark.stable
@allure.tag('Script owner : chenwei', 'Case owner : 邱大伟')
class TestContractEx_104:

    @allure.step('前置条件')
    def setup(self):
        print(''' 构造成交数据 ''')
        ATP.make_market_depth(depth_count=5)
        sell_price = ATP.get_adjust_price(1.01)
        buy_price = ATP.get_adjust_price(0.99)
        ATP.common_user_make_order(price=sell_price, direction='sell')
        ATP.common_user_make_order(price=buy_price, direction='buy')
        time.sleep(1)

    @allure.title('撮合当周 卖出平仓 部分成交多人多笔价格相同的订单     ')
    @allure.step('测试执行')
    def test_execute(self, symbol, symbol_period, DB_orderSeq):
        with allure.step('详见官方文档'):
            contracttype = 'this_week'
            leverrate = 5
            self.current = ATP.get_current_price(contract_code=symbol_period)

            res = ATP.current_user_make_order(
                contract_code=symbol_period, price=self.current, volume=5, direction="buy", offset="close")
            pprint(res)

            buy_order = contract_api.contract_order(symbol=symbol, contract_type=contracttype, price=self.current,
                                                    volume=2,
                                                    direction="sell", offset='close', lever_rate=leverrate,
                                                    order_price_type='limit')
            pprint(buy_order)

            buy_order1 = contract_api.contract_order(symbol=symbol, contract_type=contracttype, price=self.current,
                                                     volume=1,
                                                     direction="sell", offset='close', lever_rate=leverrate,
                                                     order_price_type='limit')

            pprint(buy_order1)
            buy_order2 = ATP.common_user_make_order(contract_code=symbol_period, price=self.current, volume=1,
                                                    direction='sell', offset='close')
            orderId2 = buy_order2['data']['order_id']
            orderId = buy_order1['data']['order_id']

            strStr = "select count(1) as c from t_exchange_match_result WHERE f_id = " \
                     "(select f_id from t_order_sequence where f_order_id= '%s')" % (
                         orderId2)

            # 给撮合时间，5秒内还未撮合完成则为失败
            n = 0
            while n < 5:
                isMatch = DB_orderSeq.selectdb_execute(
                    'order_seq', strStr)[0]['c']
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
        ATP.clean_market()


if __name__ == '__main__':
    pytest.main()
