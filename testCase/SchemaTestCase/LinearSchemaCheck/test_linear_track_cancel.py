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
@allure.feature('跟踪委托撤单')
class TestLinearTrackCancel:

    @allure.title('{title}')
    @pytest.mark.parametrize(*case_data())
    def test_linear_track_cancel(self,title,contract_code,lever_rate,last_price,status):
        a = t.linear_track_order(contract_code=contract_code,
                                 direction='buy',
                                 offset='open',
                                 lever_rate=lever_rate,
                                 volume='1',
                                 callback_rate='0.01',
                                 active_price=last_price-100,
                                 order_price_type='formula_price')
        time.sleep(1)
        order_id = a['data']['order_id']
        r = t.linear_track_cancel(contract_code=contract_code,
                                        order_id=order_id)
        pprint(r)
        assert r['status'] == status

if __name__ == '__main__':
    pytest.main()
