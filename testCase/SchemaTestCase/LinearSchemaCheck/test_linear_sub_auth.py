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
@allure.feature('批量设置子账户交易权限（全逐通用）')
class TestLinearSubAuth:


    @allure.title('{title}')
    @pytest.mark.parametrize(*case_data())
    def test_linear_sub_auth(self,title,sub_uid,sub_auth,status):
        r = t.linear_sub_auth(sub_uid=sub_uid,sub_auth=sub_auth)
        pprint(r)
        assert r['status'] == status



if __name__ == '__main__':
    pytest.main()
