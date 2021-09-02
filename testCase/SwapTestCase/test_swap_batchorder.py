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
@allure.feature('合约批量下单')
class TestSwapBatchorder:


    def test_swap_batchorder(self,contract_code):

        r = t.swap_batchorder({"orders_data": [{
                                        "contract_code": contract_code,
                                        "client_order_id": '',
                                        "price": '50000',
                                        "volume": '1',
                                        "direction": 'buy',
                                        "offset": 'open',
                                        "lever_rate": '5',
                                        "order_price_type": 'limit'
                                      }]
                                    })
        assert r['status'] == 'ok'


if __name__ == '__main__':
    pytest.main()