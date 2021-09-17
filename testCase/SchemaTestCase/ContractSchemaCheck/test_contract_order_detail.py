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
@allure.feature('获取订单明细信息')
class TestContractOrderDetail:



    def test_contract_order_detail(self,symbol):

        order_json = t.contract_order(symbol=symbol,
                                   contract_type='quarter',
                                   contract_code='',
                                   client_order_id='',
                                   price='',
                                   volume=1,
                                   direction='buy',
                                   offset='open',
                                   lever_rate=5,
                                   order_price_type='opponent')
        time.sleep(2)
        order_id = order_json['data']['order_id']
        created_at = order_json['ts']

        r = t.contract_order_detail(symbol=symbol,
                                    order_id=order_id,
                                    created_at=created_at,
                                    order_type='1',
                                    page_index='1',
                                    page_size='20')
        pprint(r)
        assert r['status'] == 'ok'

if __name__ == '__main__':
    pytest.main()