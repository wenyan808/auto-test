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
@allure.feature('查询用户财务记录')
class TestLinearFinancialRecord:

    def test_linear_financial_record(self,contract_code):
        r = t.linear_financial_record(margin_account=contract_code,type='',create_date='7',page_index='',page_size='')
        pprint(r)
        schema = {
            'data': {
                'financial_record': [
                    {
                        'id':int,
                        'ts':int,
                        'asset': 'USDT',
                        'contract_code': contract_code,
                        'margin_account': contract_code,
                        'face_margin_account': Or(str,None),
                        'type':int,
                        'amount':float
                    }
                ],
                'total_page':int,
                'current_page':int,
                'total_size':int
            },
            'status': 'ok',
            'ts': int
        }

        Schema(schema).validate(r)





if __name__ == '__main__':
    pytest.main()
