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
@allure.feature('查询用户品种实际可用杠杆倍数（逐仓）')
class TestLinearAvailableLevelRate:


    def test_linear_available_level_rate(self,contract_code,symbol):
        r = t.linear_available_level_rate(contract_code=contract_code)
        pprint(r)
        schema = {'data': [{'available_level_rate': str,
                           'contract_code': contract_code,
                           'margin_mode': 'isolated'}],
                 'status': 'ok',
                 'ts': int}

        Schema(schema).validate(r)


if __name__ == '__main__':
    pytest.main()



