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
@allure.feature('获取用户的合约历史成交记录(全仓)')
class TestLinearCrossMatchresults:



    @allure.title('{title}')
    @pytest.mark.parametrize(*case_data())
    def test_linear_cross_matchresults(self,title,contract_code,trade_type,create_date,page_index,page_size,status):
        r = t.linear_cross_matchresults(contract_code=contract_code,
                                          trade_type=trade_type,
                                          create_date=create_date,
                                          page_index=page_index,
                                          page_size=page_size)
        pprint(r)
        assert r['status'] == status




if __name__ == '__main__':
    pytest.main()
