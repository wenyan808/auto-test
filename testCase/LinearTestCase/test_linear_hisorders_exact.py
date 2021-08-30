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
@allure.feature('组合查询合约历史委托（逐仓）')
class TestLinearHisordersExact:

    def test_linear_hisorders_exact(self,contract_code,symbol):
        r = t.linear_hisorders_exact(contract_code=contract_code,
                                       trade_type='0',
                                       type='1',
                                       status='0',
                                       order_price_type='limit',
                                       start_time='',
                                       end_time='',
                                       from_id='',
                                        size='',
                                     direct='')
        pprint(r)
        schema = {'data': {'next_id': Or(int,None),
                              'orders': [{'contract_code': contract_code,
                                          'create_date': int,
                                          'direction': str,
                                          'fee': float,
                                          'fee_asset': 'USDT',
                                          'is_tpsl': int,
                                          'lever_rate': int,
                                          'liquidation_type': str,
                                          'margin_account': contract_code,
                                          'margin_frozen': float,
                                          'margin_mode': 'isolated',
                                          'offset': str,
                                          'order_id': int,
                                          'order_id_str': str,
                                          'order_price_type': str,
                                          'order_source': str,
                                          'order_type': int,
                                          'price': float,
                                          'profit': float,
                                          'query_id': int,
                                          'real_profit': Or(int,float),
                                          'status': int,
                                          'symbol': symbol,
                                          'trade_avg_price': Or(int,float),
                                          'trade_turnover': float,
                                          'trade_volume':float,
                                          'volume': float},],
                              'remain_size': int},
                     'status': 'ok',
                     'ts': int}
        Schema(schema).validate(r)



if __name__ == '__main__':
    pytest.main()
