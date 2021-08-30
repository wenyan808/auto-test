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
@allure.feature('查询开仓单关联的止盈止损订单详情（逐仓）')
class TestLinearRelationTpslOrder:



    def test_linear_relation_tpsl_order(self,contract_code):
        a = t.linear_order(contract_code=contract_code,
                           client_order_id='',
                           price='',
                           volume='1',
                           direction='buy',
                           offset='open',
                           lever_rate='5',
                           order_price_type='opponent',
                           tp_trigger_price='60000',
                           tp_order_price='60000',
                           tp_order_price_type='limit',
                           sl_order_price='20000',
                           sl_order_price_type='limit',
                           sl_trigger_price='20000')
        time.sleep(1)
        order_id = a['data']['order_id']
        r = t.linear_relation_tpsl_order(contract_code=contract_code,
                                         order_id=order_id)

        pprint(r)
        schema = {'data': {'canceled_at': int,
                          'client_order_id': Or(int,str,None),
                          'contract_code': contract_code,
                          'created_at': int,
                          'direction': str,
                          'fee': float,
                          'fee_asset': 'USDT',
                          'lever_rate': int,
                          'margin_account': contract_code,
                          'margin_frozen': float,
                          'margin_mode': 'isolated',
                          'offset': str,
                          'order_id': int,
                          'order_id_str': str,
                          'order_price_type': str,
                          'order_source': str,
                          'order_type': int,
                          'price': Or(int,float),
                          'profit': Or(int,float),
                          'status': int,
                          'symbol': str,
                          'tpsl_order_info': [{'canceled_at': int,
                                               'created_at': int,
                                               'direction': str,
                                               'fail_code': Or(None,str),
                                               'fail_reason': Or(None,str),
                                               'order_id': int,
                                               'order_id_str': str,
                                               'order_price': float,
                                               'order_price_type': str,
                                               'relation_order_id': str,
                                               'relation_tpsl_order_id': str,
                                               'status': int,
                                               'tpsl_order_type': str,
                                               'trigger_price': float,
                                               'trigger_type': str,
                                               'triggered_price': Or(int,float,None),
                                               'volume': float},],
                          'trade_avg_price': float,
                          'trade_turnover': float,
                          'trade_volume': int,
                          'volume': int},
                 'status': 'ok',
                 'ts': int}

        Schema(schema).validate(r)


if __name__ == '__main__':
    pytest.main()
