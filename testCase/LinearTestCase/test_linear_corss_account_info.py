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
@allure.feature('获取合约用户账户信息（全仓）')
class TestLinearCrossAccountInfo:


    def test_linear_cross_account_info(self,contract_code,symbol):
        r = t.linear_cross_account_info(margin_account='USDT')
        pprint(r)
        schema = {'data': [{'contract_detail': [{'adjust_factor': float,
                                                'contract_code': str,
                                                'lever_rate': int,
                                                'liquidation_price': Or(None,float),
                                                'margin_available': float,
                                                'margin_frozen': Or(int,float,None),
                                                'margin_position': Or(float,int),
                                                'profit_unreal': Or(float,int),
                                                'symbol': str},],
                           'margin_account': 'USDT',
                           'margin_asset': 'USDT',
                           'margin_balance': float,
                           'margin_frozen': Or(int,float,None),
                           'margin_mode': 'cross',
                           'margin_position': float,
                           'margin_static': float,
                           'profit_real': float,
                           'profit_unreal': Or(int,float),
                           'risk_rate': float,
                           'withdraw_available': float}],
                 'status': 'ok',
                 'ts': int}

        Schema(schema).validate(r)


if __name__ == '__main__':
    pytest.main()



