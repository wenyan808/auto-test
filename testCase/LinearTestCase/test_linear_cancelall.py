#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020/8/7
# @Author  : zhangranghan



from common.LinearServiceAPI import t
from tool.get_test_data import case_data
from schema import Schema,And,Or,Regex,SchemaError

from pprint import pprint
import pytest,allure,random,time



@allure.epic('正向永续')
@allure.feature('撤销全部合约单')
class TestLinearCancelall:



    @allure.title('{title}')
    @pytest.mark.parametrize(*case_data())
    def test_linear_cancelall(self,title,contract_code,status,buy_price,lever_rate):
        a = t.linear_order(contract_code=contract_code,
                       client_order_id='',
                       price=buy_price-1,
                       volume='1',
                       direction='buy',
                       offset='open',
                       lever_rate=lever_rate,
                       order_price_type='limit')
        time.sleep(1)

        r = t.linear_cancelall(contract_code=contract_code)
        pprint(r)
        assert r['status'] == status



if __name__ == '__main__':
    pytest.main()
