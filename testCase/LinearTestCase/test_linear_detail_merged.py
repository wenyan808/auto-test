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
@allure.feature('获取聚合行情')
class TestLinearDetailMerged:


    @allure.title('{title}')
    @pytest.mark.parametrize(*case_data())
    def test_linear_detail_merged(self,title,contract_code,status):
        r = t.linear_detail_merged(contract_code=contract_code)
        pprint(r)
        assert r['status'] == status


if __name__ == '__main__':
    pytest.main()
