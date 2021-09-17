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
@allure.feature('获取计划委托当前委托(全仓)')
class TestLinearCrossTriggerOpenorders:


    @allure.title('{title}')
    @pytest.mark.parametrize(*case_data())
    def test_linear_cross_trigger_openorders(self,title,contract_code,last_price,lever_rate,page_index,page_size,status):
        t.linear_cross_trigger_order(contract_code=contract_code,
                                     trigger_type='le',
                                     trigger_price=last_price-100,
                                     order_price=last_price-100,
                                     order_price_type='limit',
                                     volume='1',
                                     direction='buy',
                                     offset='open',
                                     lever_rate=lever_rate)
        time.sleep(1)
        r = t.linear_cross_trigger_openorders(contract_code=contract_code,
                                           page_index=page_index,
                                           page_size=page_size)
        pprint(r)
        assert r['status'] == status


if __name__ == '__main__':
    pytest.main()
