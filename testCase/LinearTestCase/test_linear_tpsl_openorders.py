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
@allure.feature('查询止盈止损订单当前委托（逐仓）')
class TestLinearTpslOpenorders:

    def test_linear_tpsl_openorders(self,contract_code,symbol):
        t.linear_order(contract_code=contract_code,
                           client_order_id='',
                           price='',
                           volume='1',
                           direction='buy',
                           offset='open',
                           lever_rate='5',
                           order_price_type='opponent')

        t.linear_tpsl_order(contract_code=contract_code,
                                direction='sell',
                                volume='1',
                                tp_trigger_price='60000',
                                tp_order_price='60000',
                                tp_order_price_type='limit',
                                sl_order_price='20000',
                                sl_order_price_type='limit',
                                sl_trigger_price='20000')
        time.sleep(1)

        r = t.linear_tpsl_openorders(contract_code=contract_code,
                                     page_index='',
                                     page_size='')
        pprint(r)
        schema = {'data': {'current_page': int,
                          'orders': [{'contract_code': contract_code,
                                      'created_at': int,
                                      'direction': str,
                                      'margin_account': contract_code,
                                      'margin_mode': 'isolated',
                                      'order_id': int,
                                      'order_id_str': str,
                                      'order_price': float,
                                      'order_price_type': str,
                                      'order_source': str,
                                      'order_type': int,
                                      'relation_tpsl_order_id': str,
                                      'source_order_id': Or(int,None),
                                      'status': int,
                                      'symbol': symbol,
                                      'tpsl_order_type': str,
                                      'trigger_price': float,
                                      'trigger_type': str,
                                      'volume': float},],
                          'total_page': int,
                          'total_size': int},
                 'status': 'ok',
                 'ts': int}

        Schema(schema).validate(r)


if __name__ == '__main__':
    pytest.main()
