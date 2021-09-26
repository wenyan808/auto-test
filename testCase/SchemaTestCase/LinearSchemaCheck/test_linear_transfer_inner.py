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
@allure.feature('同账号不同保证金账户的划转')
class TestLinearTransferInner:


    @allure.title('{title}')
    @pytest.mark.parametrize(*case_data())
    def test_linear_transfer_inner(self,title,asset,from_margin_account,to_margin_account,amount,status):
        r = t.linear_transfer_inner(asset=asset,from_margin_account=from_margin_account,to_margin_account=to_margin_account,amount=amount)
        pprint(r)
        assert r['status'] == status



if __name__ == '__main__':
    pytest.main()
