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
@allure.feature('获取平台阶梯保证金（逐仓）')
class TestLinearLadderMargin:



    def test_linear_ladder_margin(self,contract_code,symbol):


        r = t.linear_ladder_margin(contract_code=contract_code)
        pprint(r)
        schema = {'data': [{'contract_code': contract_code,
                           'list': [{'ladders': [{'max_margin_available': Or(int,float,None),
                                                  'max_margin_balance': Or(int,float,None),
                                                  'min_margin_available': Or(int,float,None),
                                                  'min_margin_balance': Or(int,float)},None],
                                     'lever_rate': int},],
                                   'margin_account': contract_code,
                                   'margin_mode': 'isolated',
                                   'symbol': symbol}],
                         'status': 'ok',
                         'ts': int}
        Schema(schema).validate(r)




if __name__ == '__main__':
    pytest.main()
