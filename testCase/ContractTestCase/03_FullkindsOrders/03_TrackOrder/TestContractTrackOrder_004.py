#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020/7/1
# @Author  : zhangranghan


from common.ContractServiceAPI import t as contract_api
from common.ContractServiceOrder import t as contranct_order

from schema import Schema, And, Or, Regex, SchemaError
from pprint import pprint
import pytest, allure, random, time
from tool.get_test_data import case_data


@allure.epic('反向交割')
@allure.feature('获取用户的合约账户和持仓信息')
class TestContractTrackOrder_004:

    def setUp(self):
        print('\n前置条件')

    # @allure.title('{title}')
    def test_contract_account_position_info(self, symbol, symbol_period):
        flag = True

        self.setUp()
        print('\n步骤一:获取最近价\n')
        r = contract_api.contract_history_trade(symbol=symbol_period, size='1')
        pprint(r)
        price = r['data'][0]['data'][0]['price']
        activationprice = round((price * 1.02), 1)
        callbackrate = 0.01
        triggerprice = round((activationprice * (0.99-callbackrate)), 1)



        print('\n步骤二:按激活价下单\n')

        r = contract_api.contract_track_order(symbol=symbol,
                                              contract_type='this_week',
                                              direction='sell',
                                              offset='open',
                                              lever_rate='5',
                                              volume='1',
                                              callback_rate=callbackrate,
                                              active_price=str(activationprice),
                                              order_price_type='formula_price')
        pprint(r)
        time.sleep(0.5)
        orderid = r['data']['order_id']
        print('\n步骤三:查询跟踪委托当前委托状态为未激活\n')

        r = contract_api.contract_track_openorders(symbol=symbol)
        pprint(r)

        actual_activestate = r['data']['orders'][0]['is_active']
        actual_orderid = r['data']['orders'][0]['order_id']

        if (actual_activestate != 0) or (actual_orderid != orderid):
            print("查询跟踪委托当前委托不符合预期")
            print("实际状态为：%s, 实际单号为%s" % (actual_activestate, actual_orderid))
            print("预期状态为：%s, 预期单号为%s" % (0, orderid))
            flag = False

        print('\n步骤四:控制现价到激活价格\n')

        contract_api.contract_control_price(symbol=symbol, price=activationprice,
                                            contract_type='this_week', lever_rate='5')

        print('\n步骤五:查询跟踪委托当前委托状态为已激活\n')

        r = contract_api.contract_track_openorders(symbol=symbol)
        pprint(r)

        actual_activestate2 = r['data']['orders'][0]['is_active']
        actual_orderid2 = r['data']['orders'][0]['order_id']

        if (actual_activestate2 != 1) or (actual_orderid2 != orderid):
            print("查询跟踪委托当前委托不符合预期")
            print("实际状态为：%s, 实际单号为%s" % (actual_activestate2, actual_orderid2))
            print("预期状态为：%s, 预期单号为%s" % (1, orderid))
            flag = False


        print('\n步骤六:控制现价到触发价格\n')

        contract_api.contract_control_price(symbol=symbol, price=triggerprice,
                                            contract_type='this_week', lever_rate='5')

        time.sleep(1)

        print('\n步骤七:查询当前未成交委托\n')

        r = contract_api.contract_openorders(symbol=symbol, page_index='', page_size='')
        pprint(r)

        ordersource = r['data']['orders'][0]['order_source']
        limitorderid = r['data']['orders'][0]['order_id_str']

        if ordersource != 'track':
            print("订单来源不符合预期")
            print("实际状态为：%s" %ordersource)
            print("预期状态为：track")
            flag = False

        print('\n步骤八: 查询跟踪委托历史委托\n')

        r = contract_api.contract_track_hisorders(symbol=symbol, status='0', trade_type='0', create_date='1')
        pprint(r['data']['orders'][0])

        status3 = r['data']['orders'][0]['status']
        actual_orderid3 = r['data']['orders'][0]['order_id']
        relationorderid = r['data']['orders'][0]['relation_order_id']

        if (status3 != 4) or (actual_orderid3 != orderid):
            print("查询跟踪委托历史委托不符合预期")
            print("预期订单类型：%s, 实际单号为%s" % (status3, actual_orderid3))
            print("预期订单类型：4 ，4:已委托、5:委托失败 , 预期单号为%s" % orderid)
            flag = False
        time.sleep(0.5)
        if relationorderid != limitorderid:
            print('限价单ID为', limitorderid)
            print('历史委托中的关联限价单ID为', relationorderid)
            print("历史委托中的关联限价单ID和当前存在的限价单ID不一致")
            flag = False

        print('\n恢复环境:撤单\n')

        r = contract_api.contract_cancel(symbol=symbol, order_id=limitorderid)
        pprint(r)


        assert flag == True

if __name__ == '__main__':
    pytest.main()
