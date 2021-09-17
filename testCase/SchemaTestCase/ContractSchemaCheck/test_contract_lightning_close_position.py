#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020/7/9
# @Author  : zhangranghan



from common.ContractServiceAPI import t
from tool.get_test_data import case_data
from schema import Schema,And,Or,Regex,SchemaError
from pprint import pprint
import pytest,allure,random,time



@allure.epic('反向交割')
@allure.feature('闪电平仓下单')
class TestContractLightningClosePosition:




    def test_contract_lightning_close_position(self,symbol):

        t.contract_order(symbol=symbol,
                                   contract_type='quarter',
                                   contract_code='',
                                   client_order_id='',
                                   price='',
                                   volume=1,
                                   direction='buy',
                                   offset='open',
                                   lever_rate=5,
                                   order_price_type='opponent')


        r = t.lightning_close_position(symbol=symbol,
                                       contract_type='quarter',
                                       contract_code='',
                                       client_order_id='',
                                       volume='1',
                                       direction='sell',
                                       order_price_type='')
        pprint(r)
        assert r['status'] == 'ok'



if __name__ == '__main__':
    pytest.main()
