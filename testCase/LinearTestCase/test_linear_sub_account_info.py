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
class TestLinearSubAccountInfo:

    def test_linear_sub_account_info(self,contract_code,sub_uid,symbol):
        r = t.linear_sub_account_info(contract_code=contract_code,sub_uid=sub_uid)
        pprint(r)
        schema = {
                    'data': [
                        {
                            'adjust_factor': float,
                            'contract_code': contract_code,
                            'lever_rate': int,
                            'liquidation_price': Or(int,float,None),
                            'margin_account': str,
                            'margin_asset': 'USDT',
                            'margin_available': float,
                            'margin_balance': float,
                            'margin_frozen': Or(int,float),
                            'margin_mode': 'isolated',
                            'margin_position': Or(int,float),
                            'margin_static': Or(int,float),
                            'profit_real': float,
                            'profit_unreal': Or(int,float),
                            'risk_rate': Or(float,None),
                            'symbol': symbol,
                            'transfer_profit_ratio':  Or(float,None),
                            'withdraw_available': Or(int,float)
                        }
                    ],
                    'status': 'ok',
                    'ts': int
                }

        Schema(schema).validate(r)



if __name__ == '__main__':
    pytest.main()
