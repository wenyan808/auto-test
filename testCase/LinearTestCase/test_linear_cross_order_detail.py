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
@allure.feature('获取用户的合约订单明细信息(全仓)')
class TestLinearCrossOrderDetail:



    def test_linear_cross_order_detail(self,contract_code,symbol):
        a = t.linear_cross_order(contract_code=contract_code,
                       client_order_id='',
                       price='',
                       volume='1',
                       direction='buy',
                       offset='open',
                       lever_rate='5',
                       order_price_type='opponent')
        time.sleep(1)
        order_id = a['data']['order_id']
        created_at = a['ts']


        r = t.linear_cross_order_detail(contract_code=contract_code,
                                  order_id=order_id,
                                  created_at=created_at,
                                  order_type='1',
                                  page_index='1',
                                  page_size='20')
        pprint(r)
        schema = {
                    'data': {
                        'adjust_value': Or(int,float),
                        'canceled_at': int,
                        'client_order_id': Or(str,None),
                        'contract_code': contract_code,
                        'created_at': int,
                        'current_page': int,
                        'direction': str,
                        'fee': Or(int,float),
                        'fee_asset': 'USDT',
                        'final_interest': int,
                        'instrument_price': Or(int,float),
                        'is_tpsl': Or(0,1),
                        'lever_rate': int,
                        'liquidation_type': str,
                        'margin_account': str,
                        'margin_asset': 'USDT',
                        'margin_frozen': Or(float,int),
                        'margin_mode': 'cross',
                        'offset': str,
                        'order_id': int,
                        'order_id_str': str,
                        'order_price_type': str,
                        'order_source': str,
                        'order_type': str,
                        'price': Or(int,float),
                        'profit': float,
                        'real_profit': Or(int,float),
                        'status': int,
                        'symbol': symbol,
                        'total_page': int,
                        'total_size': int,
                        'trade_avg_price': Or(int,float,None),
                        'trade_turnover': float,
                        'trade_volume': float,
                        'trades': [
                            {'created_at': int,
                             'fee_asset': 'USDT',
                             'id': str,
                             'profit': float,
                             'real_profit': float,
                             'role': str,
                             'trade_fee': float,
                             'trade_id': int,
                             'trade_price': float,
                             'trade_turnover': float,
                             'trade_volume': float}
                        ],
                        'volume': float
                    },
                    'status': 'ok',
                    'ts': int
                }

        Schema(schema).validate(r)


if __name__ == '__main__':
    pytest.main()
