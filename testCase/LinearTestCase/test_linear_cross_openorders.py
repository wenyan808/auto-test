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
@allure.feature('获取用户的合约当前未成交委托(全仓)')
class TestLinearCrossOpenorders:

    @allure.title('{title}')
    @pytest.mark.parametrize(*case_data())
    def test_linear_cross_openorders(self,title,contract_code,page_index,page_size,status,buy_price,lever_rate):
        t.linear_cross_order(contract_code=contract_code,
                       client_order_id='',
                       price=buy_price-1,
                       volume='1',
                       direction='buy',
                       offset='open',
                       lever_rate=lever_rate,
                       order_price_type='limit')
        time.sleep(1)
        r = t.linear_cross_openorders(contract_code=contract_code,
                                    page_index=page_index,
                                    page_size=page_size)
        pprint(r)
        assert r['status'] == status



if __name__ == '__main__':
    pytest.main()
