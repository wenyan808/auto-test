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
@allure.feature('批量获取最近的交易记录')
class TestLinearHistoryTrade:


    @allure.title('{title}')
    @pytest.mark.parametrize(*case_data())
    def test_linear_history_trade(self,title,contract_code,size,status):
        r = t.linear_history_trade(contract_code=contract_code,size=size)
        pprint(r)
        assert r['status'] == status


if __name__ == '__main__':
    pytest.main()
