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
@allure.feature('获取合约的历史资金费率')
class TestLinearHistoricalFundingRate:


    def test_linear_historical_funding_rate(self,contract_code,symbol):
        r = t.linear_historical_funding_rate(contract_code=contract_code,
                                             page_index='',
                                             page_size='')
        pprint(r)
        schema = {
                    'data': {
                        'current_page': int,
                        'data': [
                            {
                                'avg_premium_index': str,
                                'contract_code': contract_code,
                                'fee_asset': 'USDT',
                                'funding_rate': str,
                                'funding_time': str,
                                'realized_rate': str,
                                'symbol': symbol
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
