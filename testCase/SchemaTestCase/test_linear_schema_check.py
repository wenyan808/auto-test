#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/9/2
# @Author  : zhangranghan



from common.LinearServiceAPI import t
from tool.get_test_data import case_data
from schema import Schema,And,Or,Regex,SchemaError
from pprint import pprint
import pytest,allure



@allure.feature('正向永续字段校验')
class TestLinearSchemaCheck:

    @allure.title('获取合约用户账户信息')
    def test_linear_account_info(self,contract_code,symbol):
        r = t.linear_account_info(contract_code=contract_code)
        pprint(r)
        schema = {
            'data': [
                {
                    'adjust_factor': Or(float,int),
                    'contract_code': contract_code,
                    'lever_rate': int,
                    'margin_account': str,
                    'liquidation_price': Or(float,None),
                    'margin_asset': 'USDT',
                    'margin_available': Or(float,None),
                    'margin_balance': Or(float,None),
                    'margin_frozen': Or(float,None,int),
                    'margin_mode': 'isolated',
                    'margin_position': Or(float,None),
                    'margin_static': Or(float,None),
                    'profit_real': Or(float,None),
                    'profit_unreal': Or(float,None),
                    'risk_rate': Or(float,None),
                    'symbol': symbol,
                    'withdraw_available': Or(float,None)
                }
            ],
            'status': 'ok',
            'ts': int
        }

        Schema(schema).validate(r)


    @allure.title('获取合约用户账户持仓信息')
    def test_linear_account_position_info(self,contract_code,symbol):
        r = t.linear_account_position_info(contract_code=contract_code)
        pprint(r)
        schema = {
            'data': [
                {
                    'adjust_factor': Or(float,int),
                    'contract_code': contract_code,
                    'lever_rate': int,
                    'liquidation_price': Or(float,None),
                    'margin_account': str,
                    'margin_asset': 'USDT',
                    'margin_available': Or(float,None),
                    'margin_balance': Or(float,None),
                    'margin_frozen': Or(float,None,int),
                    'margin_mode': 'isolated',
                    'margin_position': Or(float,None),
                    'margin_static': Or(float,None),
                    'positions':Or([
                        {
                            'available': Or(float,None),
                            'contract_code': str,
                            'cost_hold': Or(float,None),
                            'cost_open': Or(float,None),
                            'direction': str,
                            'frozen': Or(float,None),
                            'last_price': Or(float,None,int),
                            'lever_rate': int,
                            'margin_account': str,
                            'margin_asset': 'USDT',
                            'margin_mode': 'isolated',
                            'position_margin': Or(float,None),
                            'profit': Or(float,None),
                            'profit_rate': Or(float,None),
                            'profit_unreal': Or(float,None),
                            'symbol': symbol,
                            'volume': Or(float,None),
                        }
                    ],None),
                    'profit_real': Or(float,None),
                    'profit_unreal': Or(float,None),
                    'risk_rate': Or(float,None),
                    'symbol': symbol,
                    'withdraw_available': Or(float,None)
                }
            ],
            'status': 'ok',
            'ts': int
        }

        Schema(schema).validate(r)






if __name__ == '__main__':
    pytest.main()
