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
@allure.feature('获取用户资产和持仓信息（全仓）')
class TestLinearCrossAccountPositionInfo:


    def test_linear_cross_account_position_info(self):
        r = t.linear_cross_account_position_info(margin_account='USDT')
        pprint(r)
        schema = {'data': {'contract_detail': [{'adjust_factor': float,
                                               'contract_code': str,
                                               'lever_rate': int,
                                               'liquidation_price': Or(None,float),
                                               'margin_available': float,
                                               'margin_frozen': Or(int,float),
                                               'margin_position': Or(int,float),
                                               'profit_unreal': Or(int,float),
                                               'symbol': str},],
                           'margin_account': 'USDT',
                           'margin_asset': 'USDT',
                           'margin_balance': Or(float,int),
                           'margin_frozen': Or(float,int),
                           'margin_mode': 'cross',
                           'margin_position': Or(float,int),
                           'margin_static': Or(float,int),
                           'positions': [{'available': Or(float,int),
                                          'contract_code': str,
                                          'cost_hold': Or(float,int),
                                          'cost_open': Or(float,int),
                                          'direction': str,
                                          'frozen': float,
                                          'last_price': Or(float,int),
                                          'lever_rate': int,
                                          'margin_account': 'USDT',
                                          'margin_asset': 'USDT',
                                          'margin_mode': 'cross',
                                          'position_margin': Or(float,int),
                                          'profit': Or(float,int),
                                          'profit_rate': Or(float,int),
                                          'profit_unreal': Or(float,int),
                                          'symbol': str,
                                          'volume': float},],
                          'profit_real': float,
                          'profit_unreal': float,
                          'risk_rate': float,
                          'transfer_profit_ratio': Or(None,int,float,str),
                          'withdraw_available': float},
                 'status': 'ok',
                 'ts': int}


        Schema(schema).validate(r)






if __name__ == '__main__':
    pytest.main()
