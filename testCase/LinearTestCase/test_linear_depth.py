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
@allure.feature('获取行情深度数据')
class TestLinearDepth:



    def test_linear_depth(self,contract_code):
        r = t.linear_depth(contract_code=contract_code,type='setp0')
        pprint(r)
        schema = {'ch': 'market.{}.depth.setp0'.format(contract_code),
                     'status': 'ok',
                     'tick': Or(None,dict),
                     'ts': int}
        Schema(schema).validate(r)

if __name__ == '__main__':
    pytest.main()
