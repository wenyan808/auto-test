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
@allure.feature('查询止盈止损订单历史委托（逐仓）')
class TestLinearTpslHisorders:

    def test_linear_tpsl_hisorders(self,contract_code,symbol):
        r = t.linear_tpsl_hisorders(contract_code=contract_code,
                                    status='0',
                                    create_date='7',
                                    page_size='',
                                    page_index='',
                                    sort_by='')
        pprint(r)
        schema = {'data': {'current_page': int,
                          'orders': [{'canceled_at': int,
                                      'contract_code': contract_code,
                                      'created_at': int,
                                      'direction': str,
                                      'fail_code': Or(str,None),
                                      'fail_reason': Or(str,None),
                                      'margin_account': contract_code,
                                      'margin_mode': 'isolated',
                                      'order_id': int,
                                      'order_id_str': str,
                                      'order_price': float,
                                      'order_price_type': str,
                                      'order_source': str,
                                      'order_type': int,
                                      'relation_order_id': str,
                                      'relation_tpsl_order_id': str,
                                      'source_order_id': Or(int,None,str),
                                      'status': int,
                                      'symbol': str,
                                      'tpsl_order_type': str,
                                      'trigger_price': float,
                                      'trigger_type': str,
                                      'triggered_price': Or(str,None),
                                      'update_time': int,
                                      'volume': float},],
                          'total_page': int,
                          'total_size': int},
                 'status': 'ok',
                 'ts': int}

        Schema(schema).validate(r)


if __name__ == '__main__':
    pytest.main()
