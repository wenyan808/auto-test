#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020/7/1
# @Author  : zhangranghan


from common.SwapServiceAPI import t as swap_api
from common.ContractServiceOrder import t as contranct_order

from schema import Schema, And, Or, Regex, SchemaError
from pprint import pprint
import pytest, allure, random, time
from tool.get_test_data import case_data


@allure.epic('反向交割')
@allure.feature('获取用户的合约账户和持仓信息')
class TestCoinswapTrackOrder_005:

    def setUp(self):
        print('\n前置条件')

    # @allure.title('{title}')
    def test_contract_account_position_info(self, contract_code):
        flag = True

        self.setUp()
        print('\n步骤一:获取最近价\n')
        r = swap_api.swap_history_trade(contract_code=contract_code, size='1')
        pprint(r)
        price = r['data'][0]['data'][0]['price']
        activationprice = round((price * 0.98), 2)
        callbackrate = 0.05
        triggerprice = round((activationprice * (1.01 + callbackrate)), 2)

        print('\n步骤二:按激活价下单\n')

        r = swap_api.swap_track_order(contract_code=contract_code,
                                      direction='buy',
                                      offset='open',
                                      lever_rate='5',
                                      volume='9999',
                                      callback_rate=callbackrate,
                                      active_price=str(activationprice),
                                      order_price_type='formula_price')
        pprint(r)
        time.sleep(0.5)
        orderid = r['data']['order_id']
        print('\n步骤三:查询跟踪委托当前委托状态为未激活\n')

        r = swap_api.swap_track_openorders(contract_code=contract_code)
        pprint(r)

        actual_activestate = r['data']['orders'][0]['is_active']
        actual_orderid = r['data']['orders'][0]['order_id']

        if (actual_activestate != 0) or (actual_orderid != orderid):
            print("查询跟踪委托当前委托不符合预期")
            print("实际状态为：%s, 实际单号为%s" % (actual_activestate, actual_orderid))
            print("预期状态为：%s, 预期单号为%s" % (0, orderid))
            flag = False

        print('\n步骤四:控制现价到激活价格\n')

        swap_api.swap_control_price(contract_code=contract_code, price=activationprice, lever_rate='5')

        print('\n步骤五:查询跟踪委托当前委托状态为已激活\n')

        r = swap_api.swap_track_openorders(contract_code=contract_code)
        pprint(r)

        actual_activestate2 = r['data']['orders'][0]['is_active']
        actual_orderid2 = r['data']['orders'][0]['order_id']

        if (actual_activestate2 != 1) or (actual_orderid2 != orderid):
            print("查询跟踪委托当前委托不符合预期")
            print("实际状态为：%s, 实际单号为%s" % (actual_activestate2, actual_orderid2))
            print("预期状态为：%s, 预期单号为%s" % (1, orderid))
            flag = False

        print('\n步骤六:控制现价到触发价格\n')

        swap_api.swap_control_price(contract_code=contract_code, price=triggerprice, lever_rate='5')

        time.sleep(0.5)

        print('\n步骤七: 查询跟踪委托历史委托\n')

        r = swap_api.swap_track_hisorders(contract_code=contract_code, status='0', trade_type='0', create_date='1')
        pprint(r['data']['orders'][0])

        status3 = r['data']['orders'][0]['status']
        actual_orderid3 = r['data']['orders'][0]['order_id']
        failreason3 = r['data']['orders'][0]['fail_reason']

        if (status3 != 5) or (actual_orderid3 != orderid) or (failreason3 != '可用担保资产不足'):
            print("查询跟踪委托历史委托不符合预期")
            print("实际订单状态：%s, 实际单号为%s, 实际失败原因为%s" % (status3, actual_orderid3, failreason3))
            print("预期订单状态：5 ，4:已委托、5:委托失败 , 预期单号为%s, 预期失败原因：可用担保资产不足" % orderid)
            flag = False

        assert flag == True


if __name__ == '__main__':
    pytest.main()
