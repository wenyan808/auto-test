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
@allure.feature('合约计划委托下单')
class TestLinearTriggerOrder:


    @allure.title('{title}')
    @pytest.mark.parametrize(*case_data())
    def test_linear_trigger_order(self,title,contract_code,trigger_type,last_price,order_price_type,volume,direction,offset,lever_rate,status):
        r = t.linear_trigger_order(contract_code=contract_code,
                                       trigger_type=trigger_type,
                                       trigger_price=last_price-100,
                                       order_price=last_price-100,
                                       order_price_type=order_price_type,
                                       volume=volume,
                                       direction=direction,
                                       offset=offset,
                                       lever_rate=lever_rate)
        pprint(r)
        assert r['status'] == status

if __name__ == '__main__':
    pytest.main()
