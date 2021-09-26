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
@allure.feature('跟踪委托下单(全仓)')
class TestLinearCrossTrackOrder:


    @allure.title('{title}')
    @pytest.mark.parametrize(*case_data())
    def test_linear_cross_track_order(self,title,contract_code,direction,offset,lever_rate,volume,callback_rate,last_price,order_price_type,status):
        r = t.linear_cross_track_order(contract_code=contract_code,
                                     direction=direction,
                                     offset=offset,
                                     lever_rate=lever_rate,
                                     volume=volume,
                                     callback_rate=callback_rate,
                                     active_price=last_price-100,
                                     order_price_type=order_price_type)
        pprint(r)
        assert r['status'] == status


if __name__ == '__main__':
    pytest.main()
