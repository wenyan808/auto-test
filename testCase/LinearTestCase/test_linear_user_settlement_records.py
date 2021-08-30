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
@allure.feature('查询用户结算记录（逐仓）')
class TestLinearUserSettlementRecords:


    def test_linear_user_settlement_records(self,contract_code,symbol):
        r = t.linear_user_settlement_records(contract_code=contract_code,
                                             start_time='',
                                             end_time='',
                                             page_size='',
                                             page_index='')
        pprint(r)
        schema = {'data': {'current_page': int,
                  'settlement_records': [{'clawback': float,
                                          'contract_code': contract_code,
                                          'fee': float,
                                          'fee_asset': 'USDT',
                                          'funding_fee': float,
                                          'margin_account': contract_code,
                                          'margin_balance': Or(float,int),
                                          'margin_balance_init': Or(float,int),
                                          'margin_mode': 'isolated',
                                          'offset_profitloss': float,
                                          'positions': [{'contract_code': contract_code,
                                                         'cost_hold': float,
                                                         'cost_hold_pre': float,
                                                         'cost_open': float,
                                                         'direction': str,
                                                         'settlement_price': float,
                                                         'settlement_profit_unreal': float,
                                                         'settlement_type': 'settlement',
                                                         'symbol': symbol,
                                                         'volume': float},],
                                          'settlement_profit_real': float,
                                          'settlement_time': int,
                                          'symbol': symbol},],
                                          'total_page': int,
                                          'total_size': int},
                                 'status': 'ok',
                                 'ts': int}

        Schema(schema).validate(r)


if __name__ == '__main__':
    pytest.main()



