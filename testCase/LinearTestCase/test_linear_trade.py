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
@allure.feature('获取市场最近成交记录')
class TestLinearTrade:


    def test_linear_trade(self,contract_code):
        r = t.linear_trade(contract_code=contract_code)
        pprint(r)
        schema = {'ch': 'market.{}.trade.detail'.format(contract_code),
                  'tick': {'data': [{'amount': str,
                                     'contract_code': contract_code,
                                     'direction': str,
                                     'id': int,
                                     'price': str,
                                     'quantity': str,
                                     'trade_turnover': str,
                                     'ts': int}],
                             'id':int,
                              'ts': int},
                      'status': 'ok',
                      'ts': int}
        Schema(schema).validate(r)



if __name__ == '__main__':
    pytest.main()
