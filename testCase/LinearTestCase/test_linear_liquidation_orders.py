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
@allure.feature('获取强平订单')
class TestLinearLiquidationOrders:


    def test_linear_liquidation_orders(self,contract_code,symbol):
        r = t.linear_liquidation_orders(contract_code=contract_code,
                                        trade_type='0',
                                        create_date='7',
                                        page_index='',
                                        page_size='50')
        pprint(r)
        schema = {
                    'data': {
                        'current_page': int,
                        'orders': [
                            {
                                'contract_code': contract_code,
                                'amount': float,
                                'trade_turnover': float,
                                'created_at': int,
                                'direction': str,
                                'offset': str,
                                'price': float,
                                'symbol': symbol,
                                'volume': Or(float,int,None)
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
