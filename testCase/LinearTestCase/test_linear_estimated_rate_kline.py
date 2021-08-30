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
@allure.feature('获取预测资金费率的K线数据')
class TestLinearEstimatedRateKline:


    def test_linear_estimated_rate_kline(self,contract_code):
        r = t.linear_estimated_rate_kline(contract_code=contract_code,period='1min',size='200')
        pprint(r)
        schema = {'ch': 'market.{}.estimated_rate.{}'.format(contract_code,'1min'),
                  'status': 'ok',
                  'data': [{'amount': str,
                           'close': str,
                           'count': str,
                           'high': str,
                           'id': int,
                           'low': str,
                           'open': str,
                           'vol': str}],
                  'ts': int}
        Schema(schema).validate(r)


if __name__ == '__main__':
    pytest.main()
