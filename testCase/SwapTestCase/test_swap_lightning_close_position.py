#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020/10/13
# @Author  : zhangranghan






from common.SwapServiceAPI import t
from tool.get_test_data import case_data
from schema import Schema,And,Or,Regex,SchemaError

from pprint import pprint
import pytest,allure,random,time


@allure.epic('反向永续')
@allure.feature('闪电平仓下单')
class TestSwapLightningClosePosition:


    def test_swap_lightning_close_position(self,contract_code):
        t.swap_order(contract_code=contract_code,
                     client_order_id='',
                     price='',
                     volume='1',
                     direction='buy',
                     offset='open',
                     lever_rate='150',
                     order_price_type='opponent')

        r = t.swap_lightning_close_position(contract_code=contract_code,
                                            volume='1',
                                            direction='sell',
                                            client_order_id='',
                                            order_price_type='')
        pprint(r)
        assert r['status'] == 'ok'



if __name__ == '__main__':
    pytest.main()
