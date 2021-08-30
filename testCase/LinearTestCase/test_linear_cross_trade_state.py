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
@allure.feature('查询系统交易权限（全仓）')
class TestLinearCrossTradeState:


    def test_linear_cross_trade_state(self,contract_code,symbol):
        r = t.linear_cross_trade_state(contract_code=contract_code)
        pprint(r)
        schema = {'data': [{'cancel': int,
                           'close': int,
                           'contract_code': contract_code,
                           'margin_account': 'USDT',
                           'margin_mode': 'cross',
                           'open': int,
                           'symbol': symbol}],
                 'status': 'ok',
                 'ts': int}
        Schema(schema).validate(r)



if __name__ == '__main__':
    pytest.main()
