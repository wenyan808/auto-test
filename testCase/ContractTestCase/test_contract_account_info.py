#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020/7/31
# @Author  : zhangranghan


from common.ContractServiceAPI import t
from tool.get_test_data import case_data
from schema import Schema,And,Or,Regex,SchemaError
from pprint import pprint
import pytest,allure
from logger import logger



@allure.epic('反向交割')
@allure.feature('获取合约用户账户信息')
class TestContractAccountInfo:

    @allure.title('测试用例标题1')
    def test_contract_account_info(self,symbol):
        r = t.contract_account_info(symbol=symbol)
        pprint(r)
        # logger.info(r)
        assert r['status'] == 'ok'

if __name__ == '__main__':
    pytest.main()

