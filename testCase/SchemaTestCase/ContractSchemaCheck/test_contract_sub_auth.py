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
@allure.feature('批量设置子账户交易权限')
class TestContractSubAuth:


    def test_contract_sub_auth(self,sub_uid):

        r = t.contract_sub_auth(sub_uid=sub_uid,sub_auth='1')
        pprint(r)
        assert r['status'] == 'ok'



if __name__ == '__main__':
    pytest.main()