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
@allure.feature('获取K线数据')
class TestLinearKline:


    def test_linear_kline(self,contract_code):
        r = t.linear_kline(contract_code=contract_code,period='1min',size='200',FROM='1',to='2')
        pprint(r)
        schema = {'ch': 'market.{}.kline.{}'.format(contract_code,'1min'),
                  'data': [{'amount': Or(float, int),
                             'close': Or(float, int),
                             'count': Or(float, int),
                             'high': Or(float, int),
                             'id': Or(float, int),
                             'low': Or(float, int),
                             'open': Or(float, int),
                             'trade_turnover': Or(float, int),
                             'vol': Or(float, int)}],
                  'status': 'ok',
                  'ts': int}
        Schema(schema).validate(r)


if __name__ == '__main__':
    pytest.main()
