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
@allure.feature('批量撤销')
class TestContractCancelall:




    def test_contract_cancelall(self,symbol):

        t.contract_order(symbol=symbol,
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


        r = t.contract_cancelall(symbol=symbol)
        pprint(r)
        assert r['status'] == 'ok'



if __name__ == '__main__':
    pytest.main()
