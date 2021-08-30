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
@allure.feature('批量获取聚合行情')
class TestLinearDetailBatchMerged:


    def test_linear_detail_batch_merged(self,contract_code):
        r = t.linear_detail_batch_merged(contract_code=contract_code)
        pprint(r)
        schema = {
                     'status': 'ok',
                     'ticks': [{  'contract_code': contract_code,
                                  'amount': str,
                                  'ask': list,
                                  'bid': list,
                                  'close': str,
                                  'count': int,
                                  'high': str,
                                  'id': int,
                                  'low': str,
                                  'open': str,
                                  'trade_turnover': str,
                                  'ts': int,
                                  'vol': str}],
                     'ts': int}
        Schema(schema).validate(r)


if __name__ == '__main__':
    pytest.main()

    