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
@allure.feature('获取市场最优挂单')
class TestLinearBBO:


    def test_linear_bbo(self,contract_code):
        r = t.linear_bbo(contract_code=contract_code)
        pprint(r)
        schema = {
                    'ticks': [{'contract_code': contract_code,
                               'ask': list,
                               'bid': list,
                               'mrid': int,
                               'ts': int}],
                    'status': 'ok',
                    'ts': int}
        Schema(schema).validate(r)


if __name__ == '__main__':
    pytest.main()
