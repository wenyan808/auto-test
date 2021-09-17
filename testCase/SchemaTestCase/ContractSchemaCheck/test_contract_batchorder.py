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
@allure.feature('批量下单')
class TestContractBatchorder:


    def test_contract_batchorder(self,symbol):


        r = t.contract_batchorder({
                                      "orders_data": [{
                                        "symbol": symbol,
                                        "contract_type": "next_week",
                                        "price": 50000,
                                        "volume": 5,
                                        "direction": "buy",
                                        "offset": "open",
                                        "lever_rate": 5,
                                        "order_price_type": "limit"
                                      }, {
                                        "symbol": symbol,
                                        "contract_type": "next_week",
                                        "price": 50000,
                                        "volume": 5,
                                        "direction": "buy",
                                        "offset": "open",
                                        "lever_rate": 5,
                                        "order_price_type": "limit"
                                      }]
                                    })
        pprint(r)
        assert r['status'] == 'ok'

if __name__ == '__main__':
    pytest.main()