#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020/8/7
# @Author  : zhangranghan



from common.LinearServiceAPI import t
from tool.get_test_data import case_data
from schema import Schema,And,Or,Regex,SchemaError

from pprint import pprint
import pytest,allure,random,time


@allure.epic('正向永续')
@allure.feature('获取平台持仓量（全逐通用）')
class TestLinearHisOpenInterest:


    @allure.title('{title}')
    @pytest.mark.parametrize(*case_data())
    def test_linear_his_open_interest(self,title,contract_code,period,size,amount_type,status):
        r = t.linear_his_open_interest(contract_code=contract_code,
                                       period=period,
                                       size=size,
                                       amount_type=amount_type)
        pprint(r)
        assert r['status'] == status



if __name__ == '__main__':
    pytest.main()
