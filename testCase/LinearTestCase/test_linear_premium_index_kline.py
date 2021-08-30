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
@allure.feature('获取溢价指数K线数据')
class TestLinearPremiumIndexKline:


    def test_linear_premium_index_kline(self,contract_code,symbol):
        r = t.linear_premium_index_kline(contract_code=contract_code,period='1min',size='200')
        pprint(r)
        schema = {'ch': 'market.{}.premium_index.{}'.format(contract_code,'1min'),
                  'data': [{'amount': str,
                             'close': str,
                             'count': str,
                             'high': str,
                             'id': int,
                             'low': str,
                             'open': str,
                             'vol': str}],
                  'status': 'ok',
                  'ts': int}
        Schema(schema).validate(r)

if __name__ == '__main__':
    pytest.main()
