#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20211028
# @Author : 
    用例标题
        撮合次周 买入平仓 部分成交单人多笔价格不同的订单       
    前置条件
        
    步骤/文本
        详见官方文档
    预期结果
        正确撮合
    优先级
        2
    用例别名
        TestContractEx_245
"""

import allure
import pytest
import time
from common.ContractServiceAPI import t as contract_api, common_user_contract_service_api as common_contract_api
from tool.atp import ATP


@allure.epic('反向交割')  # 这里填业务线
@allure.feature('撮合')  # 这里填功能
@allure.story('委托单')  # 这里填子功能，没有的话就把本行注释掉
@allure.tag('Script owner : Alex Li', 'Case owner : 邱大伟')
class TestContractEx_245:

    @allure.step('前置条件')
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, symbol, symbol_period):
        print(''' 制造成交数据 ''')
        contract_type = 'next_week'
        current = ATP.get_current_price(contract_code=symbol_period)

        res1 = common_contract_api.contract_order(symbol=symbol, contract_type=contract_type, price=current,
                                                  volume=10, direction="buy", offset="open", order_price_type='limit', lever_rate=5)
        print(res1)
        res2 = contract_api.contract_order(
            contract_code=symbol_period, contract_type=contract_type, price=current, volume=10, direction="sell", offset="open", order_price_type='limit', lever_rate=5)
        print(res2)

    @allure.title('撮合次周 买入平仓 部分成交单人多笔价格不同的订单')
    @allure.step('测试执行')
    def test_execute(self, symbol, symbol_period, DB_orderSeq):
        with allure.step('详见官方文档'):
            contract_type = 'next_week'
            current = ATP.get_current_price(contract_code=symbol_period)

            res1 = common_contract_api.contract_order(symbol=symbol, contract_type=contract_type, price=round(current *
                                                      0.99, 2), volume=2, direction="sell", offset="close", order_price_type='limit', lever_rate=5)
            print(res1)
            res2 = common_contract_api.contract_order(
                symbol=symbol, contract_type=contract_type, price=round(current*0.98, 2), volume=2, direction="sell", offset="close", order_price_type='limit', lever_rate=5)
            print(res2)

            order = contract_api.contract_order(symbol=symbol, contract_type=contract_type, price=round(current*1.01, 2),
                                                volume=5, direction="buy", offset='close', order_price_type='limit', lever_rate=5)

            order_id = order['data']['order_id']

            strStr = "select count(1) as c from t_exchange_match_result WHERE f_id = (select f_id from t_order_sequence where f_order_id= '{}')".format(
                order_id)

            # 给撮合时间，3秒内还未撮合完成则为失败
            n = 0
            while n < 3:
                isMatch = DB_orderSeq.selectdb_execute(
                    'order_seq', strStr)[0]['c']
                if 1 == isMatch:
                    break
                else:
                    n = n + 1
                    time.sleep(1)
                    print('等待处理，第' + str(n) + '次重试………………………………')
                    if n == 3:
                        assert False

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')
        ATP.clean_market()
        ATP.cancel_all_types_order()


if __name__ == '__main__':
    pytest.main()
