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
@allure.feature('获取用户资产和持仓信息')
class TestLinearPositionInfo:


    def test_linear_position_info(self,contract_code,symbol):
        r = t.linear_position_info(contract_code=contract_code)
        pprint(r)
        schema = {
            'data': [
                {
                    'symbol': symbol,
                    'contract_code': contract_code,
                    'volume': float,
                    'available': float,
                    'frozen': Or(float,None),
                    'cost_open': float,
                    'cost_hold': float,
                    'profit_unreal': float,
                    'profit_rate': float,
                    'profit': float,
                    'margin_asset': 'USDT',
                    'position_margin': float,
                    'lever_rate': int,
                    'margin_account': str,
                    'margin_mode': 'isolated',
                    'direction': str,
                    'last_price': Or(float,int)
                }
            ],
            'status': 'ok',
            'ts': int
        }

        Schema(schema).validate(r)





if __name__ == '__main__':
    pytest.main()
