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
@allure.feature('精英账户多空持仓对比-账户数')
class TestSwapEliteAccountRatio:


    def test_swap_elite_account_ratio(self,contract_code):

        r = t.swap_elite_account_ratio(contract_code=contract_code,period='60min')
        pprint(r)
        assert r['status'] == 'ok'



if __name__ == '__main__':
    pytest.main()