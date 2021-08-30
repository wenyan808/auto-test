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
@allure.feature('组合查询用户财务记录（全逐通用）')
class TestLinearFinancialRecordExact:

    def test_linear_financial_record_exact(self,contract_code):
        r = t.linear_financial_record_exact(margin_account=contract_code,
                                            contract_code=contract_code,
                                            type='',
                                            start_time='',
                                            end_time='',
                                            from_id='',
                                            size='',
                                            direct='')
        pprint(r)
        schema = {'data': {'financial_record': [{'amount': Or(float,int),
                                                'asset': 'USDT',
                                                'contract_code': contract_code,
                                                'face_margin_account': str,
                                                'id': int,
                                                'margin_account': contract_code,
                                                'ts': int,
                                                'type': int},],
                                              'next_id': int,
                                              'remain_size': int},
                                     'status': 'ok',
                                     'ts': int}

        Schema(schema).validate(r)


if __name__ == '__main__':
    pytest.main()
