#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020/3/22 11:20 AM
# @Author  : zhangranghan


from common.SwapServiceAPI import t
from tool.get_test_data import case_data
from schema import Schema,And,Or,Regex,SchemaError

from pprint import pprint
import pytest,allure,random,time


@allure.epic('反向永续')
@allure.feature('获取合约用户账户信息')
class TestSwapContractInfo:


    def test_swap_contract_info(self,contract_code):

        r = t.swap_contract_info(contract_code=contract_code)
        assert r['status'] == 'ok'



if __name__ == '__main__':
    pytest.main()