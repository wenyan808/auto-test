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
@allure.feature('切换杠杆倍数 （逐仓）')
class TestLinearSwitchLeverRate:


    def test_linear_switch_lever_rate(self,contract_code,symbol):
        r = t.linear_switch_lever_rate(contract_code=contract_code,lever_rate='5')
        pprint(r)
        schema = {'data': {'contract_code': contract_code,
                          'lever_rate': int,
                          'margin_mode': 'isolated'},
                 'status': 'ok',
                 'ts': int}

        Schema(schema).validate(r)


if __name__ == '__main__':
    pytest.main()



