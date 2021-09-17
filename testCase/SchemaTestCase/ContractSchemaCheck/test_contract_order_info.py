#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020/7/9
# @Author  : zhangranghan



from common.ContractServiceAPI import t
from tool.get_test_data import case_data
from schema import Schema,And,Or,Regex,SchemaError
from pprint import pprint
import pytest,allure,random,time



@allure.epic('反向交割')
@allure.feature('获取合约订单信息')
class TestContractOrderInfo:

    def test_contract_order_info(self,symbol):

        order_json = t.contract_order(symbol=symbol,
                                   contract_type='quarter',
                                   contract_code='',
                                   client_order_id='',
                                   price='50000',
                                   volume=1,
                                   direction='buy',
                                   offset='open',
                                   lever_rate=5,
                                   order_price_type='limit')
        time.sleep(1)
        order_id = order_json['data']['order_id']


        r = t.contract_order_info(symbol=symbol,
                                  order_id=order_id,
                                  client_order_id='')
        pprint(r)
        assert r['status'] == 'ok'

if __name__ == '__main__':
    pytest.main()