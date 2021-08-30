#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020/11/6
# @Author  : zhangranghan




from common.LinearServiceAPI import t
from tool.get_test_data import case_data
from schema import Schema,And,Or,Regex,SchemaError

from pprint import pprint
import pytest,allure,random,time



@allure.epic('正向永续')
@allure.feature('查询平台阶梯调整系数--全仓')
class TestLinearAdjustfactor:


    def test_linear_cross_adjustfactor(self):
        r = t.linear_cross_adjustfactor()
        pprint(r)
        schema = {
                    'data': [
                        {
                            'contract_code': str,
                            'list': [
                                {
                                    'ladders': [
                                        {
                                            'adjust_factor': Or(float,int,None),
                                            'ladder': Or(float,int,None),
                                            'max_size': Or(float,int,None),
                                            'min_size': Or(float,int,None),
                                        }
                                    ],
                                    'lever_rate': int
                                },

                            ],
                            'margin_mode': str,
                            'symbol': str
                        },

                    ],
                    'status': 'ok',
                    'ts': int
                }

        Schema(schema).validate(r)





if __name__ == '__main__':
    pytest.main()
