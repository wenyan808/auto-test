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
@allure.feature('获取指数的K线数据（全逐通用）')
class TestLinearHistoryIndex:


    def test_linear_history_index(self,contract_code):
        r = t.linear_history_index(symbol=contract_code,period='1min',size='10')
        pprint(r)
        schema = {'ch': 'market.{}.index.{}'.format(contract_code,'1min'),
                    'data':[
                        {'amount': Or(float,int),
                         'close': Or(int,float),
                         'count': int,
                         'high': Or(int,float),
                         'id':int,
                         'low': Or(int,float),
                         'open': Or(int,float),
                         'vol':Or(int,float)}],
                     'status': 'ok',
                     'ts': int}
        Schema(schema).validate(r)


if __name__ == '__main__':
    pytest.main()