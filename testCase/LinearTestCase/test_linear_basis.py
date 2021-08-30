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
@allure.feature('获取基差数据')
class TestLinearBasis:


    def test_linear_basis(self,contract_code):
        r = t.linear_basis(contract_code=contract_code,period='1min',basis_price_type='open',size='200')
        pprint(r)
        schema = {'ch': 'market.{}.basis.1min.open'.format(contract_code),
                    'data': [{'basis': str,
                           'basis_rate':str,
                           'contract_price': str,
                           'id': int,
                           'index_price': str}],
                    'status': 'ok',
                    'ts': int}
        Schema(schema).validate(r)


if __name__ == '__main__':
    pytest.main()
