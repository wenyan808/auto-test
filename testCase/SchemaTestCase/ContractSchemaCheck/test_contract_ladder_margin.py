#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020/7/31
# @Author  : zhangranghan


from common.ContractServiceAPI import t
from tool.get_test_data import case_data
from schema import Schema,And,Or,Regex,SchemaError
from pprint import pprint
import pytest,allure,random,time



@allure.epic('反向交割')
@allure.feature('获取平台阶梯保证金')
class TestContractLadderMargin:

    @allure.title('测试用例标题1')
    def test_contract_ladder_margin(self,symbol):

        r = t.contract_ladder_margin(symbol=symbol)
        pprint(r)
        assert r['status'] == 'ok'




if __name__ == '__main__':
    pytest.main()

