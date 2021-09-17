#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020/7/1
# @Author  : zhangranghan


from common.ContractServiceAPI import t as contranct_api
from common.ContractServiceOrder import t as contranct_order
from common.util import compare_dict

from schema import Schema, And, Or, Regex, SchemaError
from pprint import pprint
import pytest, allure, random, time
from tool.get_test_data import case_data


@allure.epic('合约自动化测试')
@allure.feature('')
@allure.title('{title}')
class TestContractLimitOrder_001:

    def setUp(self):
        print('\n前置条件')


    def test_contract_account_position_info(self, symbol, symbol_period):
        flag = True
        leverrate = '5'

        self.setUp()
        print('\n步骤一:获取最近价\n')
        r = contranct_api.contract_history_trade(symbol=symbol_period, size='1')
        pprint(r)
        lastprice = r['data'][0]['data'][0]['price']
        orderprice = round((lastprice * 0.98), 1)

        print('\n步骤二:下一个卖单\n')

        r = contranct_api.contract_order(symbol=symbol, contract_type='this_week', price=lastprice, volume='1',
                                         direction='sell', offset='open', lever_rate=leverrate,
                                         order_price_type='limit')
        pprint(r)
        time.sleep(1)
        orderid1 = r['data']['order_id']
        """获取当前冻结保证金"""
        r = contranct_api.contract_account_info(symbol=symbol)
        pprint(r)
        frozen1 = r['data'][0]['margin_frozen']
        """获取当前委托数量"""
        r = contranct_api.contract_openorders(symbol=symbol, page_index='', page_size='')
        totalsize1 = r['data']['total_size']

        print('\n步骤三:下一个低于卖一价格的买单\n')

        r = contranct_api.contract_order(symbol=symbol, contract_type='this_week', price=orderprice, volume='1',
                                         direction='buy', offset='open', lever_rate=leverrate,
                                         order_price_type='limit')
        pprint(r)
        time.sleep(0.5)

        orderid2 = r['data']['order_id']

        """获取当前冻结保证金"""
        r = contranct_api.contract_account_info(symbol=symbol)
        pprint(r)
        frozen2 = r['data'][0]['margin_frozen']
        """获取当前委托数量及详情"""
        r = contranct_api.contract_openorders(symbol=symbol, page_index='', page_size='')
        totalsize2 = r['data']['total_size']
        actual_orderinfo = r['data']['orders'][0]
        expectdic = {'symbol': symbol,
                     'order_price_type': 'limit',
                     'lever_rate': leverrate,
                     'price': orderprice,
                     'volume': '1',
                     'contract_type': 'this_week'}

        if frozen2 <= frozen1:
            print("冻结资金没有增加，不符合预期")
            flag = False

        if totalsize2 - totalsize1 != 1:
            print("当前委托数量增量不为1，不符合预期")
            flag = False
        print(expectdic)
        print(actual_orderinfo)
        if compare_dict(expectdic, actual_orderinfo) is not True:
            print("订单信息不符合预期")
            flag = False

        print('\n步骤四:撤掉刚才下的买入单\n')

        r = contranct_api.contract_cancel(symbol=symbol, order_id=orderid2)
        pprint(r)
        time.sleep(1)
        """获取历史订单"""
        r = contranct_api.contract_hisorders_exact(symbol=symbol, trade_type='1', type='2', status='7')
        pprint(r)
        actual_orderinfo2 = r['data']['orders'][0]
        if compare_dict(expectdic, actual_orderinfo2) is not True:
            print("订单信息不符合预期")
            flag = False
        """获取当前冻结保证金"""
        r = contranct_api.contract_account_info(symbol=symbol)
        pprint(r)
        frozen3 = r['data'][0]['margin_frozen']
        if frozen3 != frozen1:
            print("冻结资金没有恢复到初始状态，不符合预期")
            flag = False

        print('\n恢复环境:撤单\n')

        r = contranct_api.contract_cancel(symbol=symbol, order_id=orderid1)
        pprint(r)

        assert flag == True


if __name__ == '__main__':
    pytest.main()
