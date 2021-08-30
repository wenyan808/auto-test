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
@allure.feature('查询平台历史结算记录（全逐通用）')
class TestLinearSettlementRecords:

    def test_linear_settlement_records(self,contract_code,symbol):
        r = t.linear_settlement_records(contract_code=contract_code,
                                        start_time='',
                                        end_time='',
                                        page_size='',
                                        page_index='')
        pprint(r)
        schema = {'data': {'current_page': int,
                          'settlement_record': [{'clawback_ratio': float,
                                                 'contract_code': contract_code,
                                                 'settlement_price': float,
                                                 'settlement_time': int,
                                                 'settlement_type': 'settlement',
                                                 'symbol': symbol},],
                          'total_page': int,
                          'total_size': int},
                 'status': 'ok',
                 'ts': int}

        Schema(schema).validate(r)



if __name__ == '__main__':
    pytest.main()
