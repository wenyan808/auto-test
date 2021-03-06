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
@allure.feature('查询平台阶梯调整系数')
class TestSwapAdjustfactor:


    def test_swap_adjustfactor(self,contract_code):

        r = t.swap_adjustfactor(contract_code=contract_code)
        assert r['status'] == 'ok'



if __name__ == '__main__':
    pytest.main()