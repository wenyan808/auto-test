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
@allure.feature('止盈止损订单撤单（逐仓）')
class TestLinearTpslCancel:

    @allure.title('{title}')
    @pytest.mark.parametrize(*case_data())
    def test_linear_tpsl_cancel(self,title,contract_code,sell_price,lever_rate,last_price,status):
        t.linear_order(contract_code=contract_code,
                           client_order_id='',
                           price=sell_price,
                           volume='1',
                           direction='buy',
                           offset='open',
                           lever_rate=lever_rate,
                           order_price_type='limit')
        a = t.linear_tpsl_order(contract_code=contract_code,
                                direction='sell',
                                volume='1',
                                tp_trigger_price=last_price+100,
                                tp_order_price=last_price+100,
                                tp_order_price_type='limit',
                                sl_order_price=last_price-100,
                                sl_order_price_type='limit',
                                sl_trigger_price=last_price-100)
        time.sleep(1)
        order_id = a['data']['tp_order']['order_id']
        r = t.linear_tpsl_cancel(contract_code=contract_code,
                                 order_id=order_id)
        pprint(r)
        assert r['status'] == status


if __name__ == '__main__':
    pytest.main()
