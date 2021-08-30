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
@allure.feature('查询用户结算记录（全仓）')
class TestLinearCrossUserSettlementRecords:


    def test_linear_cross_user_settlement_records(self,contract_code,symbol):
        r = t.linear_cross_user_settlement_records(margin_account='USDT',
                                             start_time='',
                                             end_time='',
                                             page_size='',
                                             page_index='')
        pprint(r)
        schema = {'data': {'current_page': int,
                          'settlement_records': [{'clawback': float,
                                                  'contract_detail': [{'contract_code': str,
                                                                       'fee': float,
                                                                       'fee_asset': 'USDT',
                                                                       'offset_profitloss': float,
                                                                       'positions': [{'contract_code': str,
                                                                                      'cost_hold': float,
                                                                                      'cost_hold_pre': float,
                                                                                      'cost_open': float,
                                                                                      'direction': str,
                                                                                      'settlement_price': float,
                                                                                      'settlement_profit_unreal': float,
                                                                                      'settlement_type': 'settlement',
                                                                                      'symbol': str,
                                                                                      'volume': float},],
                                                                       'symbol': str},],
                                                  'fee': float,
                                                  'fee_asset': 'USDT',
                                                  'funding_fee': float,
                                                  'margin_account': 'USDT',
                                                  'margin_balance': Or(float,None),
                                                  'margin_balance_init': Or(float,None),
                                                  'margin_mode': 'cross',
                                                  'offset_profitloss': float,
                                                  'settlement_profit_real': float,
                                                  'settlement_time': int}],
                          'total_page': int,
                          'total_size': int},
                 'status': 'ok',
                 'ts': int}

        Schema(schema).validate(r)


if __name__ == '__main__':
    pytest.main()



