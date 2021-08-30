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
@allure.feature('查询合约风险准备金余额和预估分摊比例')
class TestSwapRiskInfo:


    def test_swap_risk_info(self,contract_code):

        r = t.swap_risk_info(contract_code=contract_code)
        pprint(r)
        assert r['status'] == 'ok'



if __name__ == '__main__':
    pytest.main()