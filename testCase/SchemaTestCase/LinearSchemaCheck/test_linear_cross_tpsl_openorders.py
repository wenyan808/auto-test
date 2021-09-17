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
@allure.feature('查询止盈止损订单当前委托（全仓）')
class TestLinearCrossTpslOpenorders:


    @allure.title('{title}')
    @pytest.mark.parametrize(*case_data())
    def test_linear_cross_tpsl_openorders(self,title,contract_code,sell_price,last_price,lever_rate,page_index,page_size,STATUS):
        t.linear_cross_order(contract_code=contract_code,
                           client_order_id='',
                           price=sell_price,
                           volume='1',
                           direction='buy',
                           offset='open',
                           lever_rate=lever_rate,
                           order_price_type='limit')

        t.linear_cross_tpsl_order(contract_code=contract_code,
                                direction='sell',
                                volume='1',
                                tp_trigger_price=last_price+100,
                                tp_order_price=last_price+100,
                                tp_order_price_type='limit',
                                sl_order_price=last_price-100,
                                sl_order_price_type='limit',
                                sl_trigger_price=last_price-100)
        time.sleep(1)

        r = t.linear_cross_tpsl_openorders(contract_code=contract_code,
                                         page_index=page_index,
                                         page_size=page_size)
        pprint(r)
        assert r['status'] == STATUS

if __name__ == '__main__':
    pytest.main()
