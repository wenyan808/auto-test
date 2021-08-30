#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020/8/20
# @Author  : zhangranghan



from common.SwapServiceAPI import t
from tool.get_test_data import case_data
from schema import Schema,And,Or,Regex,SchemaError

from pprint import pprint
import pytest,allure,random,time



@allure.epic('反向永续')
@allure.feature('精英账户多空持仓对比-持仓量')
class TestSwapElitePositionRatio:


    def test_swap_elite_position_ratio(self,contract_code):

        r = t.swap_elite_position_ratio(contract_code=contract_code,period='12hour')
        pprint(r)
        assert r['status'] == 'ok'



if __name__ == '__main__':
    pytest.main()