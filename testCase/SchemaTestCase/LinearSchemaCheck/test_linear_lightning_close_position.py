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
@allure.feature('合约闪电平仓下单')
class TestLinearLightningClosePosition:


    @allure.title('{title}')
    @pytest.mark.parametrize(*case_data())
    def test_linear_lightning_close_position(self,title,contract_code,sell_price,lever_rate,volume,direction,client_order_id,order_price_type,status):
        t.linear_order(contract_code=contract_code,
                       client_order_id='',
                       price=sell_price,
                       volume='1',
                       direction='buy',
                       offset='open',
                       lever_rate=lever_rate,
                       order_price_type='limit')
        time.sleep(1)

        r = t.linear_lightning_close_position(contract_code=contract_code,
                                              volume=volume,
                                              direction=direction,
                                              client_order_id=client_order_id,
                                              order_price_type=order_price_type)
        pprint(r)
        assert r['status'] == status




if __name__ == '__main__':
    pytest.main()
