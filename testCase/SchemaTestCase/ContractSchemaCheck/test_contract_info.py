#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2019/9/12 3:06 PM
# @Author  : zhangranghan

from common.ContractServiceAPI import t
from tool.get_test_data import case_data
from schema import Schema,And,Or,Regex,SchemaError
from pprint import pprint
import pytest,allure,random,time



@allure.epic('反向交割')
@allure.feature('获取合约信息')
class TestContractInfo:

    # @allure.title('参数校验')
    # @pytest.mark.parametrize('symbol',caller())
    def test_contract_info(self,symbol):
        r = t.contract_contract_info(
                                    symbol=symbol,
                                    contract_type='quarter',
                                    contract_code=''
                                )
        pprint(r)
        assert r['status'] == 'ok'





if __name__ == '__main__':
    pytest.main()
