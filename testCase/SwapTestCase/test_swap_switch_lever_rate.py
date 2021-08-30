#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020/10/13
# @Author  : zhangranghan




from common.SwapServiceAPI import t
from tool.get_test_data import case_data
from schema import Schema,And,Or,Regex,SchemaError

from pprint import pprint
import pytest,allure,random,time


@allure.epic('反向永续')
@allure.feature('切换杠杆倍数')
class TestSwapSwitchLeverRate:


    def test_swap_switch_lever_rate(self,contract_code):

        r = t.swap_switch_lever_rate(contract_code=contract_code,lever_rate='5')
        pprint(r)
        assert r['status'] == 'ok'



if __name__ == '__main__':
    pytest.main()