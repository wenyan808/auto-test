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
@allure.feature('获取用户的合约历史委托')
class TestLinearHisorders:

    def test_linear_hisorders(self,contract_code,symbol):
        r = t.linear_hisorders(contract_code=contract_code,
                               trade_type='0',
                               type='1',
                               status='0',
                               create_date='7',
                               page_index='',
                               page_size='')
        pprint(r)
        schema = {
                    'data': {
                        'current_page': int,
                        'orders': [Or(
                            {
                                'contract_code': contract_code,
                                'create_date': int,
                                'direction': str,
                                'fee': float,
                                'fee_asset': 'USDT',
                                'is_tpsl': Or(0,1),
                                'lever_rate': int,
                                'liquidation_type': str,
                                'margin_account': str,
                                'margin_asset': 'USDT',
                                'margin_frozen': Or(float,None),
                                'margin_mode': 'isolated',
                                'offset': str,
                                'order_id': int,
                                'order_id_str': str,
                                'order_price_type': int,
                                'order_source': str,
                                'order_type': int,
                                'price': float,
                                'profit': float,
                                'real_profit':Or(float,int),
                                'status': int,
                                'symbol': symbol,
                                'trade_avg_price': Or(float,int),
                                'trade_turnover': float,
                                'trade_volume': float,
                                'update_time': int,
                                'volume': float
                            },None)
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
