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
@allure.feature('查询母账户下的单个子账户持仓信息（全仓）')
class TestLinearCrossSubPositionInfo:


    def test_linear_cross_sub_position_info(self,contract_code,sub_uid):
        r = t.linear_cross_sub_position_info(contract_code=contract_code,sub_uid=sub_uid)
        pprint(r)
        schema = {
                    'data': [
                        {
                            'available': float,
                            'contract_code': contract_code,
                            'cost_hold': float,
                            'cost_open': float,
                            'direction': str,
                            'frozen': float,
                            'last_price': float,
                            'lever_rate': int,
                            'margin_asset': 'USDT',
                            'position_margin': float,
                            'profit': float,
                            'profit_rate': float,
                            'profit_unreal': float,
                            'symbol': sub_uid,
                            'volume': float
                        }
                    ],
                    'status': 'ok',
                    'ts': int
                }

        Schema(schema).validate(r)



if __name__ == '__main__':
    pytest.main()