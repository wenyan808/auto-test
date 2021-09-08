#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020/11/6
# @Author  : zhangranghan




from common.LinearServiceAPI import t
from tool.get_test_data import case_data
from schema import Schema,And,Or,Regex,SchemaError

from pprint import pprint
import pytest,allure,random,time



@allure.epic('正向永续')
@allure.feature('查询系统划转权限--全仓')
class TestLinearAdjustfactor:

    @allure.title('{title}')
    @pytest.mark.parametrize(*case_data())
    def test_linear_cross_transfer_state(self,title,margin_account,status):
        r = t.linear_cross_transfer_state(margin_account=margin_account)
        pprint(r)
        assert r['status'] == status





if __name__ == '__main__':
    pytest.main()
