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
@allure.feature('查询平台阶梯调整系数')
class TestLinearAdjustfactor:


    def test_linear_adjustfactor(self,contract_code,symbol):
        r = t.linear_adjustfactor(contract_code=contract_code)
        pprint(r)
        schema = {
                    'data': [
                        {
                            'contract_code': contract_code,
                            'list': [
                                {
                                    'ladders': [
                                        {
                                            'adjust_factor': float,
                                            'ladder': int,
                                            'max_size': Or(int,None),
                                            'min_size': Or(int,None)
                                        }
                                    ],
                                    'lever_rate': int
                                }
                            ],
                            'margin_mode': 'isolated',
                            'symbol': symbol
                        }
                    ],
                    'status': 'ok',
                    'ts': int
                }

        Schema(schema).validate(r)





if __name__ == '__main__':
    pytest.main()
