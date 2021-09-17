#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020/7/1
# @Author  : zhangranghan


from common.ContractServiceAPI import t
from tool.get_test_data import case_data
from schema import Schema,And,Or,Regex,SchemaError
from pprint import pprint
import pytest,allure,random,time



@allure.epic('反向交割')
@allure.feature('查询单个子账户资产信息')
class TestContractSubAccountInfo:


    def test_contract_sub_account_info(self,sub_uid,symbol):

        r = t.contract_sub_account_info(symbol=symbol,
                                        sub_uid=sub_uid)
        pprint(r)
        assert r['status'] == 'ok'



if __name__ == '__main__':
    pytest.main()
