#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020/10/13
# @Author  : zhangranghan



from common.SwapServiceAPI import t
from tool.get_test_data import case_data
from schema import Schema,And,Or,Regex,SchemaError

from pprint import pprint
import pytest,allure,random,time

@allure.epic('反向永续')
@allure.feature('获取订单明细信息')
class TestSwapOrderDetail:



    def test_swap_order_detail(self,contract_code):
        a = t.swap_order(contract_code=contract_code,
                         client_order_id='',
                         price='50000',
                         volume='1',
                         direction='buy',
                         offset='open',
                         lever_rate='5',
                         order_price_type='limit')
        time.sleep(2)
        order_id = a['data']['order_id']
        created_at = a['ts']

        r = t.swap_order_detail(contract_code=contract_code,
                                order_id=order_id,
                                created_at=created_at,
                                order_type='1',
                                page_index='',
                                page_size='')
        assert r['status'] == 'ok'


if __name__ == '__main__':
    pytest.main()