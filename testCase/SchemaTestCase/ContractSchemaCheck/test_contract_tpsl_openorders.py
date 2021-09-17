

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
@allure.feature('查询止盈止损订单当前委托接口')
class TestContractTpslOpenorders:


    def test_contract_tpsl_openorders(self,symbol):

        t.contract_tpsl_order(symbol=symbol,contract_type='quarter',direction='sell',volume='1',tp_order_price='50000',tp_order_price_type='limit',tp_trigger_price='60000')
        r = t.contract_tpsl_openorders(symbol=symbol)
        pprint(r)
        assert r['status'] == 'ok'



if __name__ == '__main__':
    pytest.main()