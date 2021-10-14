#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020/7/1
# @Author  : 张广南


from common.ContractServiceAPI import t as contract_api
from common.ContractServiceOrder import t as contranct_order

from schema import Schema, And, Or, Regex, SchemaError
from pprint import pprint
import pytest, allure, random, time
from tool.get_test_data import case_data


@allure.epic('反向交割')
@allure.feature('获取用户的合约账户和持仓信息')
@pytest.mark.stable
@allure.tag('Script owner : 张广南', 'Case owner : 封泰')
class TestContractTrackOrder_001:

    def setup(self):
        print('\n前置条件')

    def test_contract_account_position_info(self, symbol, symbol_period):
        flag = True
        print('\n步骤一:获取最近价\n')
        r = contract_api.contract_history_trade(symbol=symbol_period, size='1')
        pprint(r)
        price = r['data'][0]['data'][0]['price']
        activationprice = round((price * 0.98), 1)

        print('\n步骤二:按激活价下单\n')

        r = contract_api.contract_track_order(symbol=symbol,
                                              contract_type='this_week',
                                              direction='buy',
                                              offset='open',
                                              lever_rate='5',
                                              volume='1',
                                              callback_rate='0.1',
                                              active_price=str(activationprice),
                                              order_price_type='formula_price')
        pprint(r)
        time.sleep(0.5)
        orderid = r['data']['order_id']
        print('\n步骤三:查询跟踪委托当前委托\n')

        r = contract_api.contract_track_openorders(symbol=symbol)
        pprint(r)

        actual_price = r['data']['orders'][0]['active_price']
        actual_symbol = r['data']['orders'][0]['symbol']
        actual_orderid = r['data']['orders'][0]['order_id']

        if (actual_price != activationprice) or (actual_symbol != symbol) or (actual_orderid != orderid):
            print("查询跟踪委托当前委托不符合预期")
            print("实际价格为：%s, 实际币种为%s, 实际单号为%s" % (actual_price, actual_symbol, actual_orderid))
            print("预期价格为：%s, 预期币种为%s, 预期单号为%s" % (activationprice, symbol, orderid))
            flag = False

        print('\n步骤四:撤单\n')

        r = contract_api.contract_track_cancel(symbol=symbol, order_id=orderid)
        pprint(r)
        time.sleep(0.5)
        print('\n步骤五:查询跟踪委托历史委托\n')

        r = contract_api.contract_track_hisorders(symbol=symbol, status='0', trade_type='0', create_date='1')
        pprint(r['data']['orders'][0])

        actual_price2 = r['data']['orders'][0]['active_price']
        actual_symbol2 = r['data']['orders'][0]['symbol']
        actual_orderid2 = r['data']['orders'][0]['order_id']

        if (actual_price2 != activationprice) or (actual_symbol2 != symbol) or (actual_orderid2 != orderid):
            print("查询跟踪委托历史委托不符合预期")
            print("实际价格为：%s, 实际币种为%s, 实际单号为%s" % (actual_price2, actual_symbol2, actual_orderid2))
            print("预期价格为：%s, 预期币种为%s, 预期单号为%s" % (activationprice, symbol, orderid))
            flag = False

        assert flag == True

if __name__ == '__main__':
    pytest.main()
