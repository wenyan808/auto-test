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
@allure.feature('获取用户的合约订单信息')
class TestLinearOrderInfo:


    def test_linear_order_info(self,contract_code,symbol):
        a = t.linear_order(contract_code=contract_code,
                       client_order_id='',
                       price='50000',
                       volume='1',
                       direction='buy',
                       offset='open',
                       lever_rate='5',
                       order_price_type='limit')
        time.sleep(1)
        order_id = a['data']['order_id']

        r = t.linear_order_info(contract_code=contract_code,
                                order_id=order_id)
        pprint(r)
        schema = {
                    'data': [
                        {
                            'canceled_at': int,
                            'client_order_id': Or(None,int),
                            'contract_code': contract_code,
                            'created_at': int,
                            'direction': str,
                            'fee': Or(int,float),
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
                            'order_price_type': str,
                            'order_source': str,
                            'order_type': int,
                            'price': Or(int,float),
                            'profit': Or(int,float),
                            'real_profit': Or(int,float),
                            'status': int,
                            'symbol': symbol,
                            'trade_avg_price': Or(int,float,None),
                            'trade_turnover': Or(float,int),
                            'trade_volume': int,
                            'update_time': Or(int,None),
                            'volume': int
                        }
                    ],
                    'status': 'ok',
                    'ts': int
                }

        Schema(schema).validate(r)





if __name__ == '__main__':
    pytest.main()
