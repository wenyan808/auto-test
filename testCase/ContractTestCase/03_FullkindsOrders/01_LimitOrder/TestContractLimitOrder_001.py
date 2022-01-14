#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020/7/1
# @Author  : 张广南


from common.ContractServiceAPI import t as contract_api
from common.ContractServiceOrder import t as contranct_order
from common.util import compare_dict
from pprint import pprint
import pytest
import allure
import time
from tool.get_test_data import case_data
from tool.atp import ATP


@allure.epic('反向交割')
@allure.feature('现价单')
@pytest.mark.stable
class TestContractLimitOrder_001:

    def setUp(self):
        print('\n前置条件')
        ATP.clean_market()
        ATP.cancel_all_types_order()

    def test_contract_account_position_info(self, symbol, symbol_period):
        flag = True
        leverrate = '5'
        contracttype = 'this_week'

        self.setUp()
        print('\n步骤一:获取最近价\n')

        contract_code = ""
        currContractInfo = contract_api.contract_contract_info(
            symbol=symbol, contract_type=contracttype)
        contract_code = currContractInfo['data'][0]['contract_code']
        lastprice = ATP.get_redis_current_price(contract_code=contract_code)

        sellprice = round((lastprice * 1.02), 2)
        buyprice = round((lastprice * 0.99), 2)

        print('\n步骤二:下一个卖单\n')

        r = contract_api.contract_order(symbol=symbol, contract_type=contracttype, price=sellprice,
                                        volume=1, direction='sell', offset='open', lever_rate=leverrate, order_price_type='limit')
        pprint(r)
        time.sleep(1)
        orderid1 = r['data']['order_id']
        """获取当前冻结保证金"""
        r = contract_api.contract_account_info(symbol=symbol)
        pprint(r)
        frozen1 = r['data'][0]['margin_frozen']
        print("frozen1：", frozen1)
        """获取当前委托数量"""
        r = contract_api.contract_openorders(
            symbol=symbol, page_index='', page_size='')
        totalsize1 = r['data']['total_size']

        print('\n步骤三:下一个低于卖一价格的买单\n')

        r = contract_api.contract_order(symbol=symbol, contract_type=contracttype, price=buyprice,
                                        volume=1, direction='buy', offset='open', lever_rate=leverrate, order_price_type='limit')
        pprint(r)

        orderid2 = r['data']['order_id']

        """获取当前冻结保证金"""
        r = contract_api.contract_account_info(symbol=symbol)
        pprint(r)
        frozen2 = r['data'][0]['margin_frozen']
        print("frozen2：", frozen2)
        """获取当前委托数量及详情"""
        r = contract_api.contract_openorders(
            symbol=symbol, page_index='', page_size='')
        totalsize2 = r['data']['total_size']
        actual_orderinfo = r['data']['orders'][0]
        expectdic = {'symbol': symbol,
                     'order_price_type': 'limit',
                     'lever_rate': leverrate,
                     'price': buyprice,
                     'volume': 1,
                     'contract_type': contracttype}
        time.sleep(1)
        if frozen2 <= frozen1:
            print("冻结资金没有增加，不符合预期")
            flag = False

        # if totalsize2 - totalsize1 != 1:
        #     print("当前委托数量增量不为1，不符合预期")
        #     flag = False
        print(actual_orderinfo)
        if compare_dict(expectdic, actual_orderinfo) is not True:
            print("订单信息不符合预期")
            flag = False

        print('\n步骤四:撤掉刚才下的买入单\n')

        r = contract_api.contract_cancel(symbol=symbol, order_id=orderid2)
        pprint(r)
        time.sleep(1)

        """获取当前冻结保证金"""
        r = contract_api.contract_account_info(symbol=symbol)
        pprint(r)
        frozen3 = r['data'][0]['margin_frozen']
        print("frozen2：", frozen2)
        if frozen3 != frozen1:
            print("冻结资金没有恢复到初始状态，不符合预期")
            flag = False

        print('\n恢复环境:撤单\n')

        r = contract_api.contract_cancel(symbol=symbol, order_id=orderid1)
        pprint(r)

        assert flag == True


if __name__ == '__main__':
    pytest.main()
