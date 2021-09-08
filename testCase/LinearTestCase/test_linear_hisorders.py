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
@allure.feature('获取用户的合约历史委托')
class TestLinearHisorders:


    @allure.title('{title}')
    @pytest.mark.parametrize(*case_data())
    def test_linear_hisorders(self,title,contract_code,trade_type,type,status,create_date,page_index,page_size,STATUS):
        r = t.linear_hisorders(contract_code=contract_code,
                               trade_type=trade_type,
                               type=type,
                               status=status,
                               create_date=create_date,
                               page_index=page_index,
                               page_size=page_size)
        pprint(r)
        assert r['status'] == STATUS



if __name__ == '__main__':
    pytest.main()
