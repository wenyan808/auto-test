#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020/7/1
# @Author  : zhangranghan

from common.ContractServiceAPI import t
from tool.get_test_data import case_data
from schema import Schema,And,Or,Regex,SchemaError
from pprint import pprint
import pytest,allure,random,time



@allure.epic('反向交割')
@allure.feature('止盈止损订单撤单接口')
class TestContractTpslCancel:


    def test_contract_tpsl_cancel(self,symbol):

        a = t.contract_tpsl_order(symbol=symbol,contract_type='quarter',direction='sell',volume='1',tp_order_price='50000',tp_order_price_type='limit',tp_trigger_price='60000')
        r = t.contract_tpsl_cancel(symbol=symbol,order_id=a['data']['tp_order']['order_id'])
        pprint(r)
        assert r['status'] == 'ok'



if __name__ == '__main__':
    pytest.main()