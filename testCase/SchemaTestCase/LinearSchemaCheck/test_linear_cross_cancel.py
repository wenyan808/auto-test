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
@allure.feature('撤销合约订单(全仓)')
class TestLinearCrossCancel:


    @allure.title('{title}')
    @pytest.mark.parametrize(*case_data())
    def test_linear_cross_cancel(self,title,contract_code,status,buy_price,lever_rate):
        a = t.linear_cross_order(contract_code=contract_code,
                       client_order_id='',
                       price=buy_price-1,
                       volume='1',
                       direction='buy',
                       offset='open',
                       lever_rate=lever_rate,
                       order_price_type='limit')
        time.sleep(1)
        order_id = a['data']['order_id']

        r = t.linear_cross_cancel(contract_code=contract_code,
                            order_id=order_id)
        pprint(r)
        assert r['status'] == status




if __name__ == '__main__':
    pytest.main()
