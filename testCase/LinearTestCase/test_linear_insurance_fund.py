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
@allure.feature('获取风险准备金历史数据')
class TestLinearInsuranceFund:


    def test_linear_insurance_fund(self,contract_code,symbol):
        r = t.linear_insurance_fund(contract_code=contract_code,page_size='',page_index='')
        pprint(r)
        schema = {
                    'data': {
                        'contract_code': contract_code,
                        'current_page': int,
                        'symbol': symbol,
                        'tick': [
                            {
                                'insurance_fund': float,
                                'ts': int
                            }
                        ],
                        'total_page': int,
                        'total_size': int
                    },
                    'status': 'ok',
                    'ts': int
                }


        Schema(schema).validate(r)


if __name__ == '__main__':
    pytest.main()
