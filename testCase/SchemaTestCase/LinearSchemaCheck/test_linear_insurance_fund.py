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
@allure.feature('获取风险准备金历史数据')
class TestLinearInsuranceFund:


    @allure.title('{title}')
    @pytest.mark.parametrize(*case_data())
    def test_linear_insurance_fund(self,title,contract_code,page_size,page_index,status):
        r = t.linear_insurance_fund(contract_code=contract_code,page_size=page_size,page_index=page_index)
        pprint(r)
        assert r['status'] == status


if __name__ == '__main__':
    pytest.main()
