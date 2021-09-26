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
@allure.feature('精英账户多空持仓对比-账户数')
class TestLinearEliteAccountRatio:


    @allure.title('{title}')
    @pytest.mark.parametrize(*case_data())
    def test_linear_elite_account_ratio(self,title,contract_code,period,status):
        r = t.linear_elite_account_ratio(contract_code=contract_code,
                                         period=period)
        pprint(r)
        assert r['status'] == status




if __name__ == '__main__':
    pytest.main()
