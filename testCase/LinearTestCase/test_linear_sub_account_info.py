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
@allure.feature('查询母账户下的单个子账户资产信息')
class TestLinearSubAccountInfo:


    @allure.title('{title}')
    @pytest.mark.parametrize(*case_data())
    def test_linear_sub_account_info(self,title,contract_code,sub_uid,status):
        r = t.linear_sub_account_info(contract_code=contract_code,sub_uid=sub_uid)
        pprint(r)
        assert r['status'] == status



if __name__ == '__main__':
    pytest.main()
