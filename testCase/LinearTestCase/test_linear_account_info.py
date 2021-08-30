#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020/8/7
# @Author  : zhangranghan



from common.LinearServiceAPI import t
from tool.get_test_data import case_data
from schema import Schema,And,Or,Regex,SchemaError
from logger import logger
from pprint import pprint
import pytest,allure,random,time



@allure.epic('正向永续')
@allure.feature('获取合约用户账户信息')
class TestLinearAccountInfo:




    @pytest.mark.schema
    def test_linear_account_info(self,contract_code,symbol):
        r = t.linear_account_info(contract_code=contract_code)
        pprint(r)
        logger.info(r)
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


if __name__ == '__main__':
    pytest.main()



