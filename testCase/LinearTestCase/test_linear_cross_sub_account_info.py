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
@allure.feature('查询母账户下的单个子账户资产信息')
class TestLinearCrossSubAccountInfo:

    def test_linear_cross_sub_account_info(self,sub_uid):
        r = t.linear_cross_sub_account_info(margin_account='USDT',sub_uid=sub_uid)
        pprint(r)
        schema = {'data': [{'contract_detail': [{'adjust_factor': float,
                                                'contract_code': str,
                                                'lever_rate': int,
                                                'liquidation_price': Or(float,int,str,None),
                                                'margin_available': Or(int,float),
                                                'margin_frozen': Or(int,float),
                                                'margin_position': int,
                                                'profit_unreal': Or(int,float),
                                                'symbol': str},],
                           'margin_account': 'USDT',
                           'margin_asset': 'USDT',
                           'margin_balance': Or(int,float),
                           'margin_frozen': Or(int,float),
                           'margin_mode': 'cross',
                           'margin_position': int,
                           'margin_static': Or(int,float),
                           'profit_real': Or(int,float),
                           'profit_unreal': Or(int,float),
                           'risk_rate': Or(int,None,float),
                           'transfer_profit_ratio': Or(int,None,float),
                           'withdraw_available': Or(int,None,float)}],
                 'status': 'ok',
                 'ts': int}


        Schema(schema).validate(r)



if __name__ == '__main__':
    pytest.main()
