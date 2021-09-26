#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020/7/1
# @Author  : zhangranghan



from common.ContractServiceAPI import t
from schema import Schema,And,Or,Regex,SchemaError
from pprint import pprint
import pytest,allure,random,time
from tool.get_test_data import case_data



@allure.epic('反向交割')
@allure.feature('获取用户的合约账户和持仓信息')
class TestContractAccountPositionInfo:

    def setUp(self):

        print('前置条件')


    @allure.title('{title}')
    @pytest.mark.parametrize(*case_data())
    def test_contract_account_position_info(self,title,symbol,status,test):
        r = t.contract_account_position_info(symbol=symbol)
        pprint(r)
        print(test)
        print(case_data())
        assert r['status'] == status




if __name__ == '__main__':
    pytest.main()
