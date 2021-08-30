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
@allure.feature('查询合约风险准备金和预估分摊比例')
class TestLinearRiskInfo:

    def test_linear_risk_info(self,contract_code):
        r = t.linear_risk_info(contract_code=contract_code)
        pprint(r)
        schema = {
                    'data': [
                        {
                            'contract_code': contract_code,
                            'estimated_clawback': float,
                            'insurance_fund': float
                        }
                    ],
                    'status': 'ok',
                    'ts': int
                }

        Schema(schema).validate(r)



if __name__ == '__main__':
    pytest.main()
