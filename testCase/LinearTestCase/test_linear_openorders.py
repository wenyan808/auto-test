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
@allure.feature('获取用户的合约当前未成交委托')
class TestLinearOpenorders:


    def test_linear_openorders(self,contract_code,symbol):

        t.linear_order(contract_code=contract_code,
                       client_order_id='',
                       price='50000',
                       volume='1',
                       direction='buy',
                       offset='open',
                       lever_rate='5',
                       order_price_type='limit')
        time.sleep(1)


        r = t.linear_openorders(contract_code=contract_code,
                                page_index='',
                                page_size='')
        pprint(r)
        schema = {
                    'data': {
                        'current_page': int,
                        'orders': [
                            {
                                'canceled_at': Or(int,str,None),
                                'client_order_id':  Or(int,str,None),
                                'contract_code': contract_code,
                                'created_at': int,
                                'direction': str,
                                'fee': Or(int,float),
                                'fee_asset': 'USDT',
                                'is_tpsl': Or(0,1),
                                'lever_rate': int,
                                'liquidation_type': Or(str,None),
                                'margin_account': str,
                                'margin_asset': 'USDT',
                                'margin_frozen': Or(int,float,None),
                                'margin_mode': 'isolated',
                                'offset': str,
                                'order_id': int,
                                'order_id_str': str,
                                'order_price_type': str,
                                'order_source': str,
                                'order_type': int,
                                'price': Or(int,float),
                                'profit': Or(int,float),
                                'real_profit':  Or(int,float),
                                'status': int,
                                'symbol': symbol,
                                'trade_avg_price': Or(int,float,None),
                                'trade_turnover': Or(int,float,None),
                                'trade_volume': int,
                                'update_time': int,
                                'volume': int
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
